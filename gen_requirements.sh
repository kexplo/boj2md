#!/usr/bin/env bash

set -euo pipefail

# tail removes first line ('-i https://pypi.org/simple')
pipenv lock -r | tail -n +2 > requirements.txt
