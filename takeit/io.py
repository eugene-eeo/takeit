import editor
from requests import get
from collections import OrderedDict
from takeit.compat import to_b, to_s
from takeit.utils import (generate_editor_contents, parse_options,
                          get_urls, filename_and_url)


def fetch_index(package):
    r = get(package.url)
    r.raise_for_status()
    return filename_and_url(get_urls(r.text))


def get_choices(index):
    contents = to_b(generate_editor_contents(index))
    output = editor.edit(contents=contents)
    rv = OrderedDict()
    for item in parse_options(to_s(output)):
        if item not in index:
            continue
        rv[item] = index[item]
    return rv


def download_files(index):
    for path in index:
        url = index[path]
        r = get(url, stream=True)

        print("Downloading %s" % path)
        with open(path, 'wb') as fp:
            for block in r.iter_content(1024):
                fp.write(block)