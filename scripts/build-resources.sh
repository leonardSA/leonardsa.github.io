#!/bin/bash

# File              : build-resources.sh
# Author            : leonardSA <leonard.stephenauguste@gmail.com>
# Date              : 10.10.2021
# Last Modified Date: 11.10.2021
# Last Modified By  : leonardSA <leonard.stephenauguste@gmail.com>

PAGES_DIR=_pages # dir containing pages with resources
PLANTUML_JAR=./scripts/lib/plantuml.1.2021.12.jar # relative to ROOT_DIR

# ARG will be substituted
DOT_CMD="dot -Tjpg ARG -Ojpg"
PLANT_CMD="java -Djava.awt.headless=true -jar $PLANTUML_JAR -Tpng ARG"

# by pair
FILETYPE=(gv uml)
COMMANDS=("$DOT_CMD" "$PLANT_CMD")

# for every filetype
for i in "${!FILETYPE[@]}"; do  
    # search directory for files with the filetype and compile them
    for file in $(find $PAGES_DIR -name *.${FILETYPE[i]}); do
        ${COMMANDS[i]/ARG/"$file"} 2> $file.log  # substitute and execute
        if [ $? -ne 0  ]; then
            1>&2 printf "\033[1;31m[KO] %s : %s\n\033[0m" $0 $file
            exit 1
        else
            printf "\033[1;32m[OK] %s : %s\n\033[0m" $0 $file
            rm $file.log
        fi
    done
done
