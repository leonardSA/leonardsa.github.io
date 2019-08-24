#!/usr/bin/env bash

set -e 

if [ "$TRAVIS_BRANCH" != "develop" ]; then
    exit 0;
fi

# code from: https://ibugone.com/blog/2018/04/build-github-pages-with-travis-ci/
cd _site
git init
git config user.name "Travis CI"
git config user.email "travis@travis-ci.org"
git add --all
git commit --message "Auto deploy from Travis CI build $TRAVIS_BUILD_NUMBER"
git remote add deploy https://$GH_TOKEN@github.com/leonardsa/leonardsa.github.io.git >/dev/null 2>&1
git push --force deploy master >/dev/null 2>&1
