#!/usr/bin/env bash

if [ "$#" -ne 0 ]; then
  GOURCE_ARGS="$@"
else
  GOURCE_ARGS="--path ${GOURCE_REPO:-.} -${GOURCE_RESOLUTION:-1920x1024} -a ${GOURCE_AUTO_SKIP_SECONDS:-0.25} -s ${GOURCE_SECOND_PER_DAY:-0.25} --title ${GOURCE_TITLE:-Title}"
fi

echo "$GOURCE_ARGS"

gource \
    --key \
    -c 1 \
    --highlight-all-users \
    --highlight-dirs \
    --hide bloom,filenames \
    --hash-seed 9182 \
    --date-format "%Y / %m / %d [%W]" \
    --font-colour aaaaaa \
    --font-size 24 \
    --caption-size 4 \
    --colour-images \
    --output-framerate 60 \
    $GOURCE_ARGS
