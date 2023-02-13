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

from json import load as json_load
from sys import argv as sys_argv
from pathlib import Path
from subprocess import check_call

print(sys_argv)

with open('config.json', "r") as fptr:
    cfg = json_load(fptr)

LogDir = Path('/tmp/glogs').resolve()
LogDir.mkdir(exist_ok=True)

with open('gource/.mailmap', "r") as fptr:
    mailmap = fptr.read()

for repo in list(set([
    repo
    for _, job in cfg.items()
    for repo in job['tree'].keys()
])):
    idx = f"{repo.replace('/','--')}"
    check_call(['git', 'clone', f'https://{repo}', idx])
    if len(mailmap) != 0:
        with (Path(idx) / '.mailmap').open('w') as fptr:
            fptr.write(mailmap)
    authors = LogDir / f'{idx}.authors'
    check_call(f'git log --pretty="%an <%ae>" | sort | uniq > {authors}', shell=True, cwd=idx)
    check_call(['gource', '--output-custom-log', LogDir / f'{idx}.log', idx])

check_call(f'cat {LogDir!s}/*.authors | sort | uniq > {LogDir!s}/authors.mails', shell=True)
check_call(['rm', '-rf', f'{LogDir!s}/*.authors'])
