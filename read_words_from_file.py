#!/usr/bin/python

import getopt
import pickle
import sys


def main(argv):
    word_file = parse_args(argv)
    with open(word_file, 'rb') as fp:
        words = pickle.load(fp)

    print(words)


def parse_args(argv):
    help_message = 'read_words_from_file.py -f <file_name>'
    file_name = None
    try:
        opts, args = getopt.getopt(argv, "hf:", ["file_name="])
    except getopt.GetoptError:
        print(help_message)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(help_message)
            sys.exit()
        elif opt in ("-f", "--file_name"):
            file_name = arg

    if not file_name:
        print(help_message)
        sys.exit(2)

    return file_name


if __name__ == '__main__':
    main(sys.argv[1:])
