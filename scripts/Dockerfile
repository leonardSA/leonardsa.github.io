FROM    ubuntu:20.04

# python3.8 already set up in ubuntu img
# install prerequisites
RUN     apt-get update -q
RUN     apt-get install git -y -q
RUN     apt-get install python3-pip -y -q
RUN     pip3 install GitPython -q

# for running with TRAVISCI
ENV     TRAVIS_BRANCH $TRAVIS_BRANCH
# copy resource file and script
COPY    ./resources/about_template.md ./tmp/about_template.md
COPY    generate_about.py ./tmp/generate_about.py

WORKDIR ./tmp

# run script with python3.8
ENTRYPOINT ["python3"]
CMD ["generate_about.py", "./transfer", "about_template.md", "1", "--branch", "TRAVIS_BRANCH"]
