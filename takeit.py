"""
takeit - minimal script fetcher.

Usage:
    takeit [--html] <id>...
    takeit (-h | --help)
    takeit --version

Options:
    --html   Generate <script> tags
"""

import sys
import os.path as path
from collections import OrderedDict, namedtuple

import editor
from requests import get
from bs4 import BeautifulSoup
from uritemplate import expand
from docopt import docopt


if sys.version_info[0] == 3:
    to_b = lambda a: a.encode('utf-8')
    to_s = lambda a: a.decode('utf-8')
else:
    to_b = str
    to_s = unicode


QUERY_URL = 'https://cdnjs.com/libraries{/id}{/version}'
MESSAGE = "# Delete the files which you don't want downloaded\n"
Spec = namedtuple('Spec', ['id', 'version'])


def parse_package_spec(string):
    parts = string.split('==', 1)
    if len(parts) == 1:
        parts += [None]
    return Spec(*parts)


def get_urls(pkg):
    url = expand(QUERY_URL, id=pkg.id, version=pkg.version)
    res = get(url)
    res.raise_for_status()
    doc = BeautifulSoup(res.text, 'html.parser')
    for node in doc.find_all('p', class_='library-url'):
        yield str(node.string)


def get_filenames(urls):
    for url in urls:
        yield path.basename(url), url


def get_options(s_bytes):
    for line in to_s(s_bytes).splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        yield line


def choose_urls(pairs):
    pairs = OrderedDict(pairs)
    choices = editor.edit(contents=to_b(MESSAGE + '\n'.join(pairs)))
    for choice in get_options(choices):
        if choice not in pairs:
            continue
        yield choice, pairs[choice]


def generate_html(pairs):
    for _, url in pairs:
        print('<script src="%s"></script>' % url)


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
        choices.extend(pairs)

    choices = choose_urls(choices)
    if arguments['--html']:
        generate_html(choices)
        return
    fetch_scripts(choices)
