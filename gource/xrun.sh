#!/usr/bin/env sh

OUTPUT_NAME="${GOURCE_REPO:-.}/${GOURCE_NAME:-gource}"

xvfb-run --auto-servernum --server-args="-screen 0, ${GOURCE_RESOLUTION:-1920x1080}x24" \
  $(dirname "$0")/run.sh $@ -o - |
  ffmpeg -y \
    -r 60 \
    -f image2pipe \
    -probesize 100M \
    -vcodec ppm \
    -i - \
    -vcodec libx264 \
    -preset slow \
    -pix_fmt yuv420p \
    -crf 18 \
    -threads 0 \
    -bf 0 \
    "$OUTPUT_NAME".mp4

ffmpeg -sseof -0.5 -i "$OUTPUT_NAME".mp4 -update 1 -q:v 1 "$OUTPUT_NAME".jpg
