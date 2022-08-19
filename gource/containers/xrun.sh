#!/usr/bin/env sh

# Authors:
#   Unai Martinez-Corral
#
# Copyright 2021-2022 Unai Martinez-Corral <unai.martinezcorral@ehu.eus>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

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
