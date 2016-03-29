"""
takeit - minimal script fetcher.

Usage:
    takeit <id>...
    takeit (-h | --help)
    takeit --version
"""

import sys
import os.path as path
from requests import get
from bs4 import BeautifulSoup
from uritemplate import expand
from docopt import docopt
import inquirer


QUERY_URL = 'https://cdnjs.com/libraries{/id}'


def get_urls(package):
    url = expand(QUERY_URL, id=package)
    res = get(url)
    res.raise_for_status()
    doc = BeautifulSoup(res.text, 'html.parser')
    for node in doc.find_all('p'):
        if 'library-url' in node.attrs.get('class', []):
            yield str(node.string)


def choose_urls(urls):
    checkbox = inquirer.Checkbox(
        'urls',
        message='Download',
        choices=list(urls),
    )
    answers = inquirer.prompt([checkbox])
    if answers is None:
        return []
    return answers['urls']


def fetch_scripts(urls):
    for url in urls:
        r = get(url, stream=True)
        r.raise_for_status()

        filename = path.basename(url)
        print("Downloading %s " % filename)

        with open(filename, 'wb') as handle:
            for block in r.iter_content(1024):
                handle.write(block)


def main():
    arguments = docopt(__doc__, version='takeit 0.1.0')
    for item in arguments['<id>']:
        urls = get_urls(item)
        fetch_scripts(choose_urls(urls))
