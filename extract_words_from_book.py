#!/usr/bin/python

import getopt
import pickle
import sys

from selenium.webdriver import Firefox
from words_provider.googlebooks import GooglePlayBooks


def main(argv):
    output, profile, url = parse_args(argv)

    driver = Firefox(firefox_profile=profile)
    word_provider = GooglePlayBooks(url, driver)
    words = word_provider.retrieve_words()

    with open(output, 'wb') as fp:
        pickle.dump(words, fp)


def parse_args(argv):
    help_message = 'extract_words_from_book.py -u <book_url> -p <firefox_profile_path> -o <output_file>'
    url = None
    profile = None
    output = 'words.txt'
    try:
        opts, args = getopt.getopt(argv, "hu:p:o:", ["url=", "profile=", "output="])
    except getopt.GetoptError:
        print(help_message)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(help_message)
            sys.exit()
        elif opt in ("-u", "--url"):
            url = arg
        elif opt in ("-p", "--profile"):
            profile = arg
        elif opt in ("-o", "--output"):
            output = arg

    if not url or not profile:
        print(help_message)
        sys.exit(2)

    return output, profile, url


if __name__ == '__main__':
    main(sys.argv[1:])
