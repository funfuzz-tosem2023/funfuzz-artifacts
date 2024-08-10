# Scripts for FS experiments

Scripts for experiments for _Boosting Greybox Fuzzing with Function Significance_, 
including: 

## Global scripts

- `setup.sh`: setting up global envs for other experimental scripts, especially fuzz scripts. 
Use `source setup.sh` to set envs globally.
- `download-subjects.sh`: downloading real-world projects used in experiments.
- `decompress-subjects.sh`: decompress subjects in the given directory.

## Instrumentation scripts

Path: `./inst`

Scripts to build and instrument target projects (at compile time).

## Fuzz scripts

Path: `./fuzz`

Scripts to fire on various fuzz campaigns. 
Common usage: `<CAMPAIGN>: <SUBJECT> <DUR_SEC> <START_IDX> <END_IDX>`

- `<CAMPAIGN>`: path to a certain fuzz script.
- `<SUBJECT>`: path to the subject under test which has already been instrumented. 
- `<DUR_SEC>`: fuzz duration, in seconds
- `<START_IDX>`: index that the campaign starts 
- `<END_IDX>`: index that the campaign ends

## Draw scripts

Path: `./draw`

Scripts to draw figures for fuzzing evaluation.
