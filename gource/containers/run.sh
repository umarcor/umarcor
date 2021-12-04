#!/usr/bin/env sh

gource \
  --key \
  -c 0.7 \
  --highlight-users \
  --highlight-dirs \
  --hide bloom,filenames \
  --hash-seed 9182 \
  --date-format '%Y / %m / %d [%W]' \
  --font-colour aaaaaa \
  --font-size 24 \
  --caption-size 4 \
  --colour-images \
  --output-framerate 60 \
  --dir-name-depth 2 \
  --frameless \
  -"${GOURCE_RESOLUTION:-1920x1080}" \
  -a "${GOURCE_AUTO_SKIP_SECONDS:-0.05}" \
  -s "${GOURCE_SECONDS_PER_DAY:-0.15}" \
  --title "${GOURCE_TITLE:-Title}" \
  $@
