FROM    ubuntu:20.04

# python3.8 already set up in ubuntu img
# install prerequisites
RUN     apt-get update -q
RUN     apt-get install git -y -q
RUN     apt-get install python3-pip -y -q
RUN     pip3 install GitPython -q

# copy scripts
# main script
COPY    modify_pages.sh     ./tmp/modify_pages.sh 
# scripts called in main script
COPY    generate_about.py   ./tmp/generate_about.py
COPY    generate_toc.py     ./tmp/generate_toc.py

# copy resource
COPY    ./resources/about_template.md ./tmp/about_template.md

WORKDIR ./tmp

# run script with bash into python3.8 for env var interpretation
CMD ["./modify_pages.sh"]
