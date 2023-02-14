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

from pathlib import Path
from subprocess import check_call
import yaml
from json import dump as json_dump

ROOT = Path('gource').resolve()
LogDir = ROOT / 'logs'
LogDir.mkdir(exist_ok=True)

# TODO Append to the enabled list, when the workflow is triggered by an scheduled event
scheduled_only = [
    'Hitchhiker',
    'iverilog',
    'MSYS2',
    'MSYS2-all',
    'CHIPSAlliance',
    'LiteX',
    'FPGAwars'
]

enabled = [
    'EDAA',
    'EDAA-Workflows',
    'EDAA-Utilities',
    'pyTooling',
    'ghdl',
    'verilator',
    'osvvm',
    'osvb',
    'osvb-noroot',
    'HDL',
    'DBHI',
    'VUnit',
    'HDLC',
    'NEORV32',
    'CoCoTb',
    'openFPGALoader',
    'renode',
    'spf13',
    'f4pga-core',
    'F4PGA',
    'VTR',
    'YosysHQ',
    'LibreCores',
]

with (ROOT / 'config.yml').open('r') as fptr:
    cfg = yaml.load(fptr, Loader=yaml.FullLoader)
    for key in cfg:
        cfg[key]['name'] = key
    with open('config.json', "w") as fptr:
        json_dump(cfg, fptr)

    jobs = [
        job
        for key, job in cfg.items()
        if key in enabled
    ]
    print(f"::set-output name=jobs::{jobs!s}")
