#!/usr/bin/env sh

# Authors:
#   Unai Martinez-Corral
#
# Copyright 2021 Unai Martinez-Corral <unai.martinezcorral@ehu.eus>
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
