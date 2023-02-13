#!/usr/bin/env python3
#
# Authors:
#   Unai Martinez-Corral
#
# Copyright 2021-2023 Unai Martinez-Corral <unai.martinezcorral@ehu.eus>
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

# Combine logs and generate video
from pathlib import Path
from subprocess import check_call
from json import load as json_load

LogDir = Path('/tmp/glogs').resolve()
CombinedDir = LogDir.parent / 'combined'
CombinedDir.mkdir(exist_ok=True)

with open('job.json', "r") as fptr:
    job = json_load(fptr)

for repo, loc in job['tree'].items():
    logFile = f"{repo.replace('/','--')}.log"
    check_call(['cp', str(LogDir / logFile), str(CombinedDir / logFile)])
    if (loc is None) or len(loc) == 0:
        continue
    check_call(['sed', '-i', '-r', f's#(.+)\|#\\1|/{loc}#', str(CombinedDir / logFile)])

CombinedLog = CombinedDir.parent / 'combined.log'

check_call(f'cat {CombinedDir!s}/*.log | sort -n > {CombinedLog!s}', shell=True)

with CombinedLog.open('r') as fptr:
    clog = fptr.read().splitlines()
with CombinedLog.open('w') as fptr:
    fptr.write(f'{clog[0].split("|")[0]}|Gource|A|/.root\n')
    fptr.write("\n".join(clog))

check_call([
  "docker",
  "run",
  "--rm",
  "-v",
  f"{LogDir.parent!s}:/wrk",
  "-w",
  "/wrk",
  "-e", f"GOURCE_TITLE={job['title']}",
  "-e", f"GOURCE_NAME={job['name']}",
  "ghcr.io/umarcor/gource/xrun",
  "/xrun.sh",
] + (job['args'] if 'args' in job else []) + [
  "combined.log"
])

print(f"::set-output name=name::{job['name']!s}")
artifact = LogDir.parent / f'{job["name"]}'
print(f"::set-output name=artifact::{artifact!s}")
