#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : generate_toc.py
# Author            : leonardSA <leonard.stephenauguste@gmail.com>
# Date              : 10.10.2021
# Last Modified Date: 15.10.2021
# Last Modified By  : leonardSA <leonard.stephenauguste@gmail.com>
# Description       : Generate table of contents for markdown.

import re
import os
import sys
import argparse
from typing import List

MIN_TITLE_CONST = 2     # 2 #s for min title e.g. ## A title
HTML_LINK = "<a name =\"{}\"></a>"
TOC_SYM = '{:toc}'


def main():
    args = parse_args()
    if os.path.exists(args.infile) is False:
        raise FileNotFoundError("File does not exist")
    generate_toc(args.infile, args.outfile)
    return 0


def parse_args():
    """
    Parses arguments.
    """
    parser = argparse.ArgumentParser(description="""Generate table of contents\
                                                    for markdown file""")
    parser.add_argument('infile', help='Path to markdown file')
    parser.add_argument('outfile', help='Path for generated markdown file')
    args = parser.parse_args()
    return args


def toc_was_called(text: str) -> int:
    """
    Verifies if toc was called.

    Raises: Warning on symbol not found.

    Returns: index of toc symbol.
    """
    count = 0
    for line in text:
        if line.find(TOC_SYM) == 0:
            toc_line = count
            return count
        count = count + 1

    raise Warning("toc: symbol not found")


def titles_get(text: str) -> List:
    """
    Fetches all titles, in order, in markdown file.

    Returns: list of (line index, title text).
    """
    titles = []
    finder = re.compile('^#+')

    count = 0   # line index
    for line in text:
        res = finder.match(line)
        if res is not None:
            titles.append((count, line))
        count = count + 1

    return titles


def format_prefix(prefix):
    """
    Formats the prefix list of a title.

    e.g. [1, 2, 1, 0] = 1.2.1.
    """
    res = ''
    for n in prefix:
        if n == 0:
            break
        res = res + '{}.'.format(n)
    return res


def format_toc(titles: List) -> List:
    """
    Formats table of contents's lines.

    Returns: list of table of content's lines.
    """
    toc = []
    prefix = [0]  # [1, 1, 2] == 1.1.2

    for no, line in titles:
        title = '[' + line.split('#')[-1].strip() + ']'

        depth = line.count('#') - MIN_TITLE_CONST
        if len(prefix) == depth:
            prefix.append(0)
        prefix[depth] = prefix[depth] + 1

        # reset title non used prefix
        for i in range(depth + 1, len(prefix)):
            prefix[i] = 0

        tag = '(#{})'.format(no)
        toc.append((depth * '\t') + (depth != 0) * '- '
                   + format_prefix(prefix) + ' ' + title + tag)

    toc.append('\n')  # leave a space -- optional
    return toc


def generate_toc(fin: str, fout: str) -> None:
    """
    Generates the table of contents.
    """
    text = None
    with open(fin, 'r') as f:
        text = f.readlines()

    # inspect text
    toc_idx = toc_was_called(text)
    titles = titles_get(text)

    # format text
    toc = format_toc(titles)

    # register modifications:
    # - for titles
    for no, line in titles:
        text[no] = line.strip() + HTML_LINK.format(no) + '\n'
    # - for toc
    text[toc_idx] = '\n'.join(toc)
    # - into file
    with open(fout, 'w') as f:
        f.writelines(text)


if __name__ == "__main__":
    main()
