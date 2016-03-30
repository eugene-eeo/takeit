import os
from collections import OrderedDict
from bs4 import BeautifulSoup


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
    content = [MESSAGE]
    content.extend(filenames)
    return '\n'.join(content)


def flatten(indexes):
    u = OrderedDict()
    for item in indexes:
        u.update(item)
    return u


def generate_html(urls):
    for item in urls:
        yield '<script src="%s"></script>' % item
