"""
takeit - minimal script fetcher.

Usage:
    takeit [--html] <id>...
    takeit (-h | --help)
    takeit --version

Options:
    --html   Generate <script> tags
"""

from docopt import docopt
from takeit.package import Package
from takeit.io import fetch_index, get_choices, download_files
from takeit.utils import flatten


# [String] -> [Package]
# [Package] -> {filename: url}
# {F: U} -choice-> {F: U}
# {F: U} -download-> Response

def main():
    args = docopt(__doc__, version='takeit 0.1.0')
    specs = args['<id>']
    html_mode = args['--html']

    packages = [Package.from_string(spec) for spec in specs]
    indexes = [fetch_index(pkg) for pkg in packages]

    index = flatten(indexes)
    index = get_choices(index)

    if html_mode:
        for _, url in index:
            print('<script src="%s"></script>' % url)
        return

    download_files(index)
