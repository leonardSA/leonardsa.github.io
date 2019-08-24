#!/usr/bin/env bash

set -e 

if [ "$TRAVIS_BRANCH" != "develop" ]; then
    exit 0;
fi

# Init
mkdir deploy_dir
cd deploy_dir
git init
git config --global user.email 'travis@travis-ci.org'
git config --global user.name 'Travis'
# Fetch repo
git remote add deploy $GITHUB_TOKEN@github.com:leonardSA/leonardsa.github.io.git
git fetch --all
# Copy gh-pages and push
git checkout gh-pages
git branch -D master
git checkout -b master
git push --force deploy master
