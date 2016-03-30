import takeit.utils
from itertools import chain


def test_get_urls():
    html = '''
    <html>
    <body>
        <p class='library-url'>one</p>
        <p class='library-url'>two</p>
    </body>
    </html>
    '''
    assert list(takeit.utils.get_urls(html)) == ['one', 'two']


def test_filename_and_url():
    urls = [
        'https://abc.net/url.js',
        'https://abc.net/two.js',
    ]
    given = dict(takeit.utils.filename_and_url(urls))
    expected = {
        'url.js': urls[0],
        'two.js': urls[1],
    }
    assert given == expected


def test_parse_options():
    given = takeit.utils.parse_options('''
    # not included
    # not included too
    one!
    two#
    ''')
    expected = ['one!', 'two#']
    assert list(given) == expected


def test_generate_editor_contents():
    files = ['abc', 'def']
    given = takeit.utils.generate_editor_contents(files)
    assert given == '\n'.join([takeit.utils.MESSAGE] + files)


def test_flatten():
    f = [(1, 1), (2, 2)]
    g = [(3, 3), (4, 4)]

    indexes = list([f, g])
    index = takeit.utils.flatten(indexes)

    assert list(index) == f + g
