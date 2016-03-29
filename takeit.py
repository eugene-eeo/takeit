"""
takeit - minimal script fetcher.

Usage:
    takeit <id>...
    takeit (-h | --help)
    takeit --version
"""

import sys
import os.path as path
import logging
from collections import OrderedDict

from requests import get
from bs4 import BeautifulSoup
from uritemplate import expand
from docopt import docopt
import inquirer


LOGGER = logging.getLogger(__name__)
QUERY_URL = 'https://cdnjs.com/libraries{/id}'


def get_urls(package):
    url = expand(QUERY_URL, id=package)
    res = get(url)
    res.raise_for_status()
    doc = BeautifulSoup(res.text, 'html.parser')
    for node in doc.find_all('p'):
        if 'library-url' in node.attrs.get('class', []):
            yield str(node.string)


def get_filenames(urls):
    for url in urls:
        yield path.basename(url), url


def choose_urls(pairs):
    pairs = OrderedDict(pairs)
    res = inquirer.prompt([inquirer.Checkbox(
        'urls',
        message='Download',
        choices=list(pairs),
    )])
    if res is None:
        return
    for item in res['urls']:
        yield item, pairs[item]


def fetch_scripts(pairs):
    for filename, url in pairs:
        r = get(url, stream=True)
        r.raise_for_status()

        LOGGER.info("Downloading %s" % filename)
        with open(filename, 'wb') as handle:
            for block in r.iter_content(1024):
                handle.write(block)


def main():
    LOGGER.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    LOGGER.addHandler(ch)

    arguments = docopt(__doc__, version='takeit 0.1.0')
    for item in arguments['<id>']:
        pairs = get_filenames(get_urls(item))
        fetch_scripts(choose_urls(pairs))
