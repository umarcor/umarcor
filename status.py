#!/usr/bin/env python3

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

from pathlib import Path
from textwrap import shorten
from urllib.parse import quote
from tabulate import tabulate

watch = {
    'HDL': {
        'hdl/awesome': {
            'doc': [
                ['asciidoctor', 'hdl.github.io/awesome']
            ],
        },
        'hdl/constraints': {
            'doc': [
                ['asciidoctor', 'hdl.github.io/constraints']
            ],
        },
        'hdl/smoke-tests': {
        },
        'hdl/containers': {
            'doc': [
                ['asciidoctor', 'hdl.github.io/containers']
            ],
        },
        'hdl/MINGW-packages': {
            'doc': [
                ['asciidoctor', 'hdl.github.io/MINGW-packages']
            ],
        },
        'hdl/Termux-packages': {
        },
    },
    'MSYS2': {
        'msys2/setup-msys2': {
        }
    },
    'GHDL': {
        'ghdl/ghdl': {
            'doc': [
                ['Read-The-Docs', 'ghdl.github.io/ghdl']
            ],
        },
        'ghdl/ghdl-cosim': {
            'doc': [
                ['Read-The-Docs', 'ghdl.github.io/ghdl-cosim']
            ],
        },
        'ghdl/ghdl-yosys-plugin': {
        },
        'ghdl/ghdl-language-server': {
        },
        'ghdl/docker': {
        },
        'ghdl/setup-ghdl-ci': {
        },
        'ghdl/extended-tests': {
        },
    },
    'VUnit': {
        'VUnit/vunit': {
            'doc': [
                ['Read-The-Docs', 'vunit.github.io']
            ],
        },
        'VUnit/tdd-intro': {
        },
        'VUnit/vunit_action': {
        },
        'VUnit/cosim': {
            'doc': [
                ['Read-The-Docs', 'vunit.github.io/cosim']
            ],
        },
        'Paebbels/JSON-for-VHDL': {
        }
    },
    'OSVG': {
        'VHDL/news': {
            'doc': [
                ['Hugo', 'vunit.github.io/cosim']
            ],
        },
        'VHDL/Compliance-Tests': {
        },
        'VHDL/pyVHDLModel': {
            'doc': [
                ['Read-The-Docs', 'vhdl.github.io/pyVHDLModel']
            ],
        }
    },
    'DBHI': {
        'dbhi/dbhi': {
            'doc': [
                ['Vue.js', 'dbhi.github.io']
            ],
        },
        'dbhi/qus': {
            'doc': [
                ['Rstudio', 'dbhi.github.io/qus']
            ],
        },
        'dbhi/docker': {
        },
        'dbhi/run': {
        },
        'dbhi/gRPC': {
        },
        'dbhi/vboard': {
        },
        'dbhi/binhook': {
        },
        'dbhi/mdpaper': {
            'doc': [
                ['Rstudio', 'dbhi.github.io/mdpaper']
            ],
        },
        'dbhi/vsc-hdl': {
        },
        'spf13/cobra': {
        }
    },
    'umarcor': {
        'umarcor/umarcor': {
            'doc': [
                ['GitHub-Sponsors', 'umarcor.github.io/umarcor']
            ],
        },
        'umarcor/OSVB': {
            'doc': [
                ['Read-The-Docs', 'umarcor.github.io/osvb']
            ],
        },
        'umarcor/SIEAV': {
            'doc': [
                ['asciidoctor', 'umarcor.github.io/SIEAV']
            ],
        },
        'umarcor/hwstudio': {
            'doc': [
                ['asciidoctor', 'umarcor.github.io/hwstudio/doc']
            ],
        },
        'umarcor/warmboot': {
            'doc': [
                ['asciidoctor', 'umarcor.github.io/warmboot']
            ],
        }
    },
    'BTD': {
        'buildthedocs/BTD': {
            'doc': [
                ['Read-The-Docs', 'buildthedocs.github.io/btd']
            ],
        },
        'buildthedocs/sphinx.theme': {
            'doc': [
                ['Read-The-Docs', 'buildthedocs.github.io/sphinx.theme']
            ],
        },
        'buildthedocs/docker': {
        }
    },
    'eine': {
        'eine/tip': {
        },
        'eine/issue-runner': {
            'doc': [
                ['Hugo', 'eine.github.io/issue-runner']
            ],
        }
    },
    'FOMU': {
        'im-tomu/fomu-workshop': {
            'doc': [
                ['Read-The-Docs', 'workshop.fomu.im'],
                ['Read-The-Docs', 'im-tomu.github.io/fomu-workshop'],
            ],
        },
        'im-tomu/fomu-toolchain': {
        },
        'im-tomu/foboot': {
        }
    },
    'EDA': {
        'gtkwave/gtkwave': {
            'doc': [
                ['Sourceforge', 'gtkwave.sourceforge.net']
            ],
        },
        'verilator/verilator': {
            'doc': [
                ['', 'verilator.org']
            ],
        },
        'steveicarus/iverilog': {
        },
    },
}


def repoShield(repo):
    logo = 'GitHub'
    host = 'github.com'
    items = repo.split(':')
    #print(items)
    if len(items)>1:
        if items[0] != 'gh':
            # TODO Implement other hosts
            host = host
        repo = items[1]
    return f'<a href="https://{host}/{repo}" ><img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/{repo}?longCache=true&style=flat-square&label={repo}&logo={logo}"></a>'


def docShields(items):
    return ' '.join([
            f'<a href="https://{item[1]}" ><img alt="Site" src="https://img.shields.io/website.svg?label={item[1]}&longCache=true&style=flat-square&logo={item[0]}&logoColor=fff&url=http%3A%2F%2F{quote(item[1])}%2Findex.html"></a>'
            for item in items
        ])


def ciShields(items):
    return 'TODO'


def otherShields(items):
    return 'TODO'


content = {}

for key, group in watch.items():
    content[key] = []
    for item, row in group.items():
        keys = row.keys()
        content[key].append([
            repoShield(item),
            (docShields(row['doc']) if 'doc' in keys else ''),
            (ciShields(row['ci']) if 'ci' in keys else ''),
            (otherShields(row['other']) if 'other' in keys else ''),
        ])

with Path('status.html').open('w') as fptr:

    fptr.write("""
<html style="background: #555">
<body>
    """)

    for key, group in watch.items():
        fptr.write(tabulate(
            content[key],
            tablefmt='unsafehtml'
        ))
        fptr.write('<hr>')

    fptr.write("""
</body>
</html>
    """)
