#!/bin/bash

# Build up fair fuzz benchmark. 

if [ $# -lt 1 ]; then
  echo "<DOWNLOAD-SUBJECTS>: <TARGET_DIR>"
  exit 1
fi

TARGET_DIR="$1"

# Each item: <download_url> <out_filename>
SUBJECTS=(
  # FairFuzz-same
  "https://github.com/libjpeg-turbo/libjpeg-turbo/archive/refs/tags/1.5.1.tar.gz"                               "libjpeg-turbo-1.5.1.tar.gz"
  "https://sourceforge.net/projects/libpng/files/libpng16/older-releases/1.6.29/libpng-1.6.29.tar.gz/download"  "libpng-1.6.29.tar.gz"
  "https://github.com/the-tcpdump-group/tcpdump/archive/refs/tags/tcpdump-4.9.0.tar.gz"                         "tcpdump-4.9.0.tar.gz"
  "https://ftp.gnu.org/gnu/binutils/binutils-2.28.tar.gz"                                                       "binutils-2.28.tar.gz"
  "https://mupdf.com/downloads/archive/mupdf-1.9-source.tar.gz"                                                 "mupdf-1.9.tar.gz"
  "https://github.com/GNOME/libxml2/archive/refs/tags/v2.9.4.tar.gz"                                            "libxml2-2.9.4.tar.gz"
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
