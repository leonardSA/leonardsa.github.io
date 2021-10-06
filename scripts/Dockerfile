FROM    ubuntu:20.04

# python3.8 already set up in ubuntu img
# install prerequisites
RUN     apt-get update -q
RUN     apt-get install git -y -q
RUN     apt-get install python3-pip -y -q
RUN     pip3 install GitPython -q

# copy resource file and script
COPY    ./resources/about_template.md ./tmp/about_template.md
COPY    generate_about.py ./tmp/generate_about.py

WORKDIR ./tmp

# run script with bash into python3.8 for env var interpretation
CMD python3 generate_about.py ./transfer about_template.md 1 --branch $TRAVIS_BRANCH
