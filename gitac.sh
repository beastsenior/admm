#!/bin/bash

set -v on
git add -A
git commit -m $(date "+%Y%m%d")+$(date "+%H%M%S")

