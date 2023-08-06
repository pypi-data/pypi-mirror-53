# -*- coding: utf-8 -*-

import argparse
import subprocess


def clone(repo_url):
    return subprocess.call(["git", "clone", repo_url])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u", "--update", help="Repository URL", required="True"
    )
    args = parser.parse_args()
    clone(args.update)


if __name__ == '__main__':
    main()
