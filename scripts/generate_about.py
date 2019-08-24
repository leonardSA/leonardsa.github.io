"""
    Generate about.md.

    Author: Joseph Leonard Stephen Auguste
    Creation date: 23/08/2019
"""

import os
import git
import time
import argparse
from typing import List

FRONT_MATTER =  """ ---
                    layout: page
                    title: About
                    permalink: /about/
                    ---
                """


def main():
    """
        Entry function.
    """
    args = parse_args()
    commits = get_commits_list(args.path, args.branch, args.nb_commits)
    if not commits:
        return 1
    footer = generate_footer(commits)
    generate_about_md(args.path, FRONT_MATTER, footer, args.template)
    return 0


def parse_args():
    """ Parses arguments.
    """
    parser = argparse.ArgumentParser(description='Generate about.md.')
    parser.add_argument('path', help='Path for about.md')
    parser.add_argument('template', help='Filename to about\'s future contents')
    parser.add_argument('nb_commits', type=int,
                        help='Number of commits to show (at least 1)')
    parser.add_argument('--branch', default="master",
                        help='Select branch for commits')
    args = parser.parse_args()
    args
    return args


def get_commits_list(repo_path: str, branch: str, nb_commits: int) -> List:
    """
        Get the nb_commits last commits and their dates.
        Formats the commits' data.
        Returns list(sha, message, date).
    """
    commits = []
    repo = git.Repo(repo_path)
    for c in repo.iter_commits('master', max_count=nb_commits):
        sha = c.hexsha[:7]
        msg = c.message.split('\n')[0]
        date = time.strftime("%d/%m/%y @ %H:%M", time.gmtime(c.committed_date))
        commits.append({"sha": sha, "msg": msg, "date": date})
    return commits


def generate_footer(commits: List) -> List:
    """
        Generate footer with commits.

        Return footer as List of String.
    """
    footer = []
    first = commits.pop(0)
    footer.append("\n\n\n**Last modified on:** {}  \n".format(first['date']))
    footer.append("**Version:** {}  \n".format(first['sha']))
    footer.append("**Message:** {}  \n\n".format(first['msg']))
    if not commits:
        return footer
    footer.append("**Last commits:**\n")
    for c in commits:
        footer.append("- **{0}:** {2:<60} ({1}) \n".format(c['sha'], c['date'], c['msg']))
    return footer


def generate_about_md(path: str, header: str, footer: str, template: str) -> None:
    """
        Write about.md with a header, a template and a footer.
    """
    about = [line.strip() + '\n' for line in FRONT_MATTER.split('\n')]
    with open(template, 'r') as f:
        about = about + f.readlines()
    about = about + footer
    with open(os.path.join(path, 'about.md'), 'w') as f:
        f.writelines(about)


if __name__ == "__main__":
    main()
