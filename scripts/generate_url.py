#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : generate_url.py
# Author            : leonardSA <leonard.stephenauguste@gmail.com>
# Date              : 19.10.2021
# Last Modified Date: 19.10.2021
# Last Modified By  : leonardSA <leonard.stephenauguste@gmail.com>
# Description       : Generates a url for markdown file.

import re
import argparse
from typing import List


TAG = '{:url}'
QUALIFIER = 'url:'
FRONT_MATTER = '---'


def main():
    args = parse_args()
    for filepath in args.files:
        url = generate_url(filepath, args.basedir)
        insert_url(filepath, url)


def generate_url(filepath, basedir):
    """
    Generates url removing basedir.
    """
    if basedir[-1] == '/':
        del basedir[-1]
    filepath = filepath.replace(basedir, '')    # rm basedir from url
    filepath = filepath.split('/')
    del filepath[-1]                            # rm filename from url
    return '/'.join(filepath) + '/'             # directory is url


def insert_url(filepath, url):
    """
    Inserts url in file.

    Raises:
        SyntaxError on TAG not found in FRONT MATTER.
    """
    with open(filepath, 'r') as f:
        text = f.readlines()

    no = 0
    while (no < len(text) and
           FRONT_MATTER not in text[no]):   # skip to where the tag should be
        no = no + 1
    no = no + 1                             # skip FRONT MATTER tag
    while (no < len(text) and
           FRONT_MATTER not in text[no]):   # and search until next tag
        if TAG in text[no]:                 # tag found => replace w/ url and w
            text[no] = text[no].replace(TAG, QUALIFIER + ' ' + url)
            with open(filepath, 'w') as f:
                f.writelines(text)
            return 0
        no = no + 1

    # TAG was not found in FRONT MATTER error
    raise SyntaxError("TAG: {} is not set in FRONT MATTER: {}".format(
                      TAG, FRONT_MATTER))


def parse_args():
    """
    Parses arguments.
    """
    parser = argparse.ArgumentParser(description="""Generates url\
                                                    for markdown file""")
    parser.add_argument('files', nargs='+',
                        help='List of paths to markdown files')
    parser.add_argument('-b', '--basedir', default='_pages',
                        help="""Base directory to substract from url.\
                                \nDefault is _pages.""")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
