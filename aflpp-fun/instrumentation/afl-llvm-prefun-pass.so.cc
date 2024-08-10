//===-- afl-llvm-prefun-pass.cpp - preprocessing for FS ---===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
//
// Coverage instrumentation done on LLVM IR level, works with Sanitizers.
//
//===----------------------------------------------------------------------===//

#include "llvm/Transforms/Instrumentation/SanitizerCoverage.h"
#include "llvm/ADT/ArrayRef.h"
#include "llvm/ADT/SmallVector.h"
#include "llvm/ADT/Triple.h"
#include "llvm/Analysis/EHPersonalities.h"
#include "llvm/Analysis/PostDominators.h"
#include "llvm/IR/CFG.h"
#include "llvm/IR/Constant.h"
#include "llvm/IR/DataLayout.h"
#include "llvm/IR/DebugInfo.h"
#include "llvm/IR/Dominators.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/GlobalVariable.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/InlineAsm.h"
#include "llvm/IR/IntrinsicInst.h"
#include "llvm/IR/Intrinsics.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/MDBuilder.h"
#include "llvm/IR/Mangler.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/PassManager.h"
#include "llvm/IR/Type.h"
#include "llvm/InitializePasses.h"
#include "llvm/Support/CommandLine.h"
#include "llvm/Support/Debug.h"
#include "llvm/Support/SpecialCaseList.h"
#include "llvm/Support/VirtualFileSystem.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/Transforms/Instrumentation.h"
#include "llvm/Transforms/Utils/BasicBlockUtils.h"
#include "llvm/Transforms/Utils/ModuleUtils.h"
#include "llvm/Passes/PassPlugin.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/IR/PassManager.h"

#include "config.h"
#include "debug.h"
#include "afl-llvm-common.h"

// Standard libs
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <list>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

using namespace llvm;

#define DEBUG_TYPE "prefun"

namespace {

// Also llvm
SanitizerCoverageOptions OverrideFromCL(SanitizerCoverageOptions Options) {

  // Sets CoverageType and IndirectCalls.
  // SanitizerCoverageOptions CLOpts = getOptions(ClCoverageLevel);
  Options.CoverageType =
      SanitizerCoverageOptions::SCK_Edge;  // std::max(Options.CoverageType,
                                           // CLOpts.CoverageType);
  Options.IndirectCalls = false;           // CLOpts.IndirectCalls;
  Options.TraceCmp = false;                //|= ClCMPTracing;
  Options.TraceDiv = false;                //|= ClDIVTracing;
  Options.TraceGep = false;                //|= ClGEPTracing;
  Options.TracePC = false;                 //|= ClTracePC;
  Options.TracePCGuard = true;             // |= ClTracePCGuard;
  Options.Inline8bitCounters = 0;          //|= ClInline8bitCounters;
  // Options.InlineBoolFlag = 0; //|= ClInlineBoolFlag;
  Options.PCTable = false;     //|= ClCreatePCTable;
  Options.NoPrune = false;     //|= !ClPruneBlocks;
  Options.StackDepth = false;  //|= ClStackDepth;
  if (!Options.TracePCGuard && !Options.TracePC &&
      !Options.Inline8bitCounters && !Options.StackDepth /*&&
      !Options.InlineBoolFlag*/)
    Options.TracePCGuard = true;  // TracePCGuard is default.

  return Options;

}

class PreFunAFL
    : public PassInfoMixin<PreFunAFL> {

 /// C++ ctor
 public:
  PreFunAFL(
      const SanitizerCoverageOptions &Options = SanitizerCoverageOptions())
      : Options(OverrideFromCL(Options)) {

  }

  // Declaration and definition are separate.
  PreservedAnalyses run(Module &M, ModuleAnalysisManager &MAM);

 private:
  // @FUN: Traverse the module and write call relations and CFGs to local.
  void extractProgramInfo(Module &M);

  unsigned getSrcLineNum(Instruction &I);

  std::string prepareOutDir();

  // Member field
  SanitizerCoverageOptions Options;

};

}  // end of namespace

#if LLVM_VERSION_MAJOR >= 11                        /* use new pass manager */

extern "C" ::llvm::PassPluginLibraryInfo LLVM_ATTRIBUTE_WEAK
llvmGetPassPluginInfo() {

  return {LLVM_PLUGIN_API_VERSION, "FunPreprocessor", "v0.1",
          /* lambda to insert our pass into the pass pipeline. */
          [](PassBuilder &PB) {

  #if LLVM_VERSION_MAJOR <= 13
            using OptimizationLevel = typename PassBuilder::OptimizationLevel;
  #endif
            PB.registerOptimizerLastEPCallback(
                [](ModulePassManager &MPM, OptimizationLevel OL) {

                  MPM.addPass(PreFunAFL());

                });

          }};

}

#endif

PreservedAnalyses PreFunAFL::run(Module                &M,
                                 ModuleAnalysisManager &MAM) {

  FUN_LOG("Run pre-fun-pass!");

  if (getenv("AFL_DEBUG")) debug = 1;

  // Traverse module and record.
  extractProgramInfo(M);
  if (debug) SAYF("Finish extractProgramInfo\n");

  // Do not preserve any analyses.
  return PreservedAnalyses::none();

}

/// Extract call relations and function names.
void PreFunAFL::extractProgramInfo(Module &M) {

  // Show plugin name.
  if ((isatty(2) && !getenv("AFL_QUIET")) || debug)
    SAYF(cCYA "FunPreprocessor" VERSION cRST "\n");
  else
    be_quiet = 1;

  // Prepare directory to output program info.
  std::string outDir = prepareOutDir();
  // ofstream: <filename>, <mode>. For mode, `out`=w(riting), `app`=a(ppend)
  std::ofstream bbNameFile(outDir + "/bbNames",
                           std::ofstream::out | std::ofstream::app);
  std::ofstream bbCallFile(outDir + "/bbCalls",
                           std::ofstream::out | std::ofstream::app);
  std::ofstream funcNameFile(outDir + "/funcNames",
                             std::ofstream::out | std::ofstream::app);

  // Record source filename.
  std::string srcFilename = M.getSourceFileName();
  FUN_LOG("Visiting src file: `%s`", srcFilename.c_str());

  // Traverse functions
  FUN_LOG("Traverse functions: ");
  for (auto &F: M) {

    if (debug)
      FUN_LOG("Find function: `%s`", F.getName().str().c_str());

    // Skip functions ignored by aflpp.
    if (isIgnoreFunction(&F)) continue;

    // Extract function name, assign it a number and output into file.
    std::string funcName = F.getName().str();
    funcNameFile << funcName << "\n";
    FUN_LOG("Write function: `%s`", funcName.c_str());

    // Traverse basic blocks
    for (auto &BB: F) {

      // Record BB name.
      std::string bbName("");

      // Traverse instructions in this BB.
      for (auto &I: BB) {

        // Get line number
        unsigned srcLineNum = getSrcLineNum(I);

        // Source code line number cannot be 0
        if (srcLineNum == 0) continue;

        // Mark BB at its first instruction.
        if (bbName.empty()) {

          bbName = srcFilename + ":" + std::to_string(srcLineNum);
          bbNameFile << bbName << "\n";
          FUN_LOG("Write BB: `%s`", bbName.c_str());

        }

        // Deal with call instructions, record call relation if current
        // instruction is a call site.
        // (LLVM DOC: about dyn_cast)
        // The dyn_cast<> operator is a “checking cast” operation. It checks to
        // see if the operand is of the specified type, and if so, returns a
        // pointer to it (this operator does not work with references). If the
        // operand is not of the correct type, a null pointer is returned.
        // `CallBase` is the base class for llvm `InvokeInst` and `CallInst`
        if (auto *c = dyn_cast<CallBase>(&I)) {

          // Debug
          if (debug) errs() << "Call:" << I << "\n";

          if (auto *callee = c->getCalledFunction()) {

            // Debug
            if (debug) SAYF("Has called function: `%s`\n",
                            callee->getName().str().c_str());

            if (!isIgnoreFunction(callee)) {

              // Call relation: caller (this bb_name), callee (name of CalledF)
              // Write into file, format: `bbName,callerFunc,calleeFunc`
              std::string callRelation
                  = bbName + "," + funcName + "," + callee->getName().str();
              bbCallFile << callRelation << "\n";
              FUN_LOG("Write call relation: `%s`",
                   callRelation.c_str());

            }
          }

        } // End of handling calls

      } // End of traversing instructions

    } // End of traversing BBs


  }

}

/// Configure directory for outputting program information
std::string PreFunAFL::prepareOutDir() {

  // Prepare directory to output program info.
  std::string outDir = "/tmp/fun";

  // Read outDir from envs.
  if (getenv(FUN_TEMP_DIR)) outDir = getenv(FUN_TEMP_DIR);

  // Create if out directory does not exist.
  struct stat st = {0};
  if (stat(outDir.c_str(), &st) == -1) {
    mkdir(outDir.c_str(), 0700);
    FUN_LOG("Create non-existent dir: `%s`", outDir.c_str());
  }

  FUN_LOG("Use fun-temp-dir: `%s`", outDir.c_str());

  return outDir;

}

/// Convenient util to get line number for an `Instruction`
unsigned PreFunAFL::getSrcLineNum(Instruction &I) {

  if (DILocation *dILoc = I.getDebugLoc()) { // Here I is an LLVM instruction

    // Get line number.
    unsigned ln = dILoc->getLine();

    // Debug
    if (debug) {
      /*
        How to handle line number from other file? Example: calling atoi, clang
        will optimize the method call to `strtol` as the content of atoi is
        `return strtol(xxx)`. The line number of the tail call inst will be
        '363', which is the location of atoi in `stdlib.h`.
      */
      // TODO: any defensive operations or filtering rules?

      std::string filename = dILoc->getFilename().str();

      // Logging
      SAYF("----------------------------------------------------------\n");
      errs() << "Inst:" << I << "\n";
      SAYF("dILoc=%d, filename=%s\n", ln, filename.c_str());
      SAYF("----------------------------------------------------------\n");

    }

    // Return line number.
    return ln;

  }

  return 0;

}
