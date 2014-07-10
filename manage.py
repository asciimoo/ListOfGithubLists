#!/usr/bin/env python

from os.path import realpath, dirname
from operator import itemgetter
from sys import exit
DIR_NAME = realpath(dirname(realpath(__file__)))


def argparser():
    import argparse
    argp = argparse.ArgumentParser(description='ListOfGithubLists update script')
    argp.add_argument('-f', '--file'
                     ,help      = 'Output file - default is README.md'
                     ,metavar   = 'FILE'
                     ,default   = DIR_NAME + '/README.md'
                     )
    subparsers = argp.add_subparsers(help='sub-command help', dest='action')
    parser_add = subparsers.add_parser('add', help='add new link')
    parser_add.add_argument('title'
                     ,metavar   = 'TITLE'
                     ,help      = 'TITLE string'
                     )
    parser_add.add_argument('url'
                     ,metavar   = 'URL'
                     ,help      = 'URL string'
                     )
    return argp.parse_args()


def __main__():
    args = argparser()
    #print(args.file)
    lines = open(args.file, 'r').readlines()
    links = {}
    header = ''
    for line in lines:
        if line.startswith(' * ['):
            title, url = line.strip()[3:-1].split('](')
            links[url] = title
        else:
            header += line
    if args.action == 'add':
        if not args.url in links:
            links[args.url] = args.title
        else:
            print('[!] item already exists')
            exit(1)
        with open(args.file, 'w') as outfile:
            outfile.write(header)
            outfile.write('\n'.join(' * [{0}]({1})'.format(title, url)
                                    for url, title
                                    in sorted(links.items(), key=itemgetter(1))))
            print('{0} added'.format(args.title))
        exit(0)


if __name__ == '__main__':
    __main__()
