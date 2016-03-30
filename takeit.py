"""
takeit - minimal script fetcher.

Usage:
    takeit <id>...
    takeit (-h | --help)
    takeit --version
"""

import sys
import os.path as path
from collections import OrderedDict, namedtuple

from requests import get
from bs4 import BeautifulSoup
from uritemplate import expand
from docopt import docopt
import inquirer


QUERY_URL = 'https://cdnjs.com/libraries{/id}{/version}'
Spec = namedtuple('Spec', ['id', 'version'])


def parse_package_spec(string):
    parts = string.split('==', 1)
    if len(parts) == 1:
        parts += [None]
    return Spec(*parts)


def get_urls(pkg):
    url = expand(QUERY_URL, id=pkg.id, version=pkg.version)
    print(url)
    res = get(url)
    res.raise_for_status()
    doc = BeautifulSoup(res.text, 'html.parser')
    for node in doc.find_all('p', class_='library-url'):
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

        print("Downloading %s" % filename)
        with open(filename, 'wb') as handle:
            for block in r.iter_content(1024):
                handle.write(block)


def main():
    arguments = docopt(__doc__, version='takeit 0.1.0')
    choices = []
    for item in arguments['<id>']:
        pkg = parse_package_spec(item)
        pairs = get_filenames(get_urls(pkg))
        choices.extend(choose_urls(pairs))
    fetch_scripts(choices)
