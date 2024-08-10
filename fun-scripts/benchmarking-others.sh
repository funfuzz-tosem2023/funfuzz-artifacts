#!/bin/bash

# Build up fair fuzz benchmark. 

if [ $# -lt 1 ]; then
  echo "<DOWNLOAD-SUBJECTS>: <TARGET_DIR>"
  exit 1
fi

TARGET_DIR="$1"

# Each item: <download_url> <out_filename>
SUBJECTS=(
  # Others
  "https://github.com/libming/libming/archive/refs/tags/ming-0_4_8.tar.gz"            "libming-0_4_8.tar.gz"
  "https://github.com/cesanta/mjs/archive/refs/tags/2.20.0.tar.gz"                    "mjs-2.20.0.tar.gz"
  "https://mujs.com/downloads/mujs-1.2.0.tar.gz"                                      "mujs-1.2.0.tar.gz"
  "https://github.com/jasper-software/jasper/archive/refs/tags/version-3.0.6.tar.gz"  "jasper-3.0.6.tar.gz"
  "http://download.osgeo.org/libtiff/tiff-4.4.0.tar.gz"                               "libtiff-4.4.0.tar.gz"
  "https://dl.xpdfreader.com/xpdf-4.04.tar.gz"                                        "xpdf-4.04.tar.gz"
)

pushd "$TARGET_DIR" || exit 1

echo "================================================"
echo "Start to download subjects into $PWD..."
echo "================================================"
echo ""

# ${#SUBJECTS[@]} for arr length
for((i=0;i<${#SUBJECTS[@]};i+=2))
do
  URL=${SUBJECTS[$i]}
  O_NAME=${SUBJECTS[$((i+1))]}

  echo "Download: URL=$URL O_NAME=$O_NAME"
  wget "$URL" -O "./$O_NAME"

  echo "------------------------------------------------"

done;

popd || exit 1

echo "Downloading subjects done."
