#!/bin/bash

set -v on
git add -A
git commit -m $(date "+%Y%m%d")_$(date "+%H%M%S")

