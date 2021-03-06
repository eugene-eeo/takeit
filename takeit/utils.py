import os
from bs4 import BeautifulSoup
from itertools import chain


MESSAGE = "# Delete the files which you don't want downloaded"


def get_urls(html):
    doc = BeautifulSoup(html, 'html.parser')
    for node in doc.find_all('p', class_='library-url'):
        yield str(node.string)


def filename_and_url(urls):
    for url in urls:
        yield os.path.basename(url), url


def parse_options(string):
    for line in string.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        yield line


def generate_editor_contents(filenames):
    return '\n'.join(chain([MESSAGE], filenames))


def generate_html(filename):
    _, ext = os.path.splitext(filename)
    if ext == '.js':
        return '<script src="%s"></script>' % (filename,)

    if ext == '.css':
        return '<link rel="stylesheet" href="%s" />' % (filename,)

    return '<!-- %s -->' % (filename,)
