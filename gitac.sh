#!/bin/bash

set -v on
git update-index --skip-worktree data/
git add -A
git commit -m $(date "+%Y%m%d")_$(date "+%H%M%S")

git remote add origin https://github.com/beastsenior/admm.git
git push origin master
