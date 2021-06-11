#!/bin/sh

xvfb-run --auto-servernum --server-args="-screen 0, ${RESOLUTION}x24" \
  $(dirname "$0")/run.sh -o - |
  ffmpeg -y \
    -r 60 \
    -f image2pipe \
    -probesize 100M \
    -vcodec ppm \
    -i - \
    -vcodec libx264 \
    -preset ultrafast \
    -pix_fmt yuv420p \
    -crf 10 \
    -threads 0 \
    -bf 0 \
    /tmp/gource.mp4

cp /tmp/gource.mp4 "$REPO/gource.mp4"

#    --highlight-users \
#    --padding 1.28 \
#    --user-scale 4.0 \
#    --font-size 24 \
#    --dir-name-depth 1 \
#--file-extensions \

#ffmpeg -y  -r 60 -f image2pipe -vcodec ppm -i output.ppm -vcodec libx264 -threads 0 -r 24000/1001 -b 6144k -bt 8192k -pass 1 -flags +loop -me_method dia -g 250 -qcomp 0.6 -qmin 10 -qmax 51 -qdiff 4 -bf 16 -b_strategy 1 -i_qfactor 0.71 -cmp +chroma -subq 1 -me_range 16 -coder 1 -sc_threshold 40 -flags2 -bpyramid-wpred-mixed_refs-dct8x8+fastpskip -keyint_min 25 -refs 1 -trellis 0 -directpred 1 -partitions -parti8x8-parti4x4-partp8x8-partp4x4-partb8x8 -an output.vid