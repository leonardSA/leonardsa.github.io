#!/bin/bash
# File              : modify_pages.sh
# Author            : leonardSA <leonard.stephenauguste@gmail.com>
# Date              : 15.10.2021
# Last Modified Date: 15.10.2021
# Last Modified By  : leonardSA <leonard.stephenauguste@gmail.com>
# Description       : Docker-runned script for modifying pages.

ROOT=./transfer         # root dir of website
PAGES_DIR=$ROOT/_pages  # _pages dir of website
TOC_SYM='{:toc}'        # table of contents' symbol

# Generate about page
python3 generate_about.py $ROOT about_template.md 1 --branch $TRAVIS_BRANCH

# Generate table of contents
for page in $(find $PAGES_DIR -name *.markdown); do  # for every markdown file
    # select only file containing the toc symbol
    if $(grep -xq "[ ]*$TOC_SYM" $page); then
        python3 generate_toc.py $page $page
    fi
done
