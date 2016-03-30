import takeit
from bs4 import BeautifulSoup


def test_get_filenames():
    given = [
        'https://co.it/file1.txt',
        'http://co.it/file2.js',
        'weird/{}',
        'handled/!.js',
    ]
    result = list(takeit.get_filenames(given))
    u = [a for a,_ in result]
    v = [b for _,b in result]
    assert u == ['file1.txt', 'file2.js', '{}', '!.js']
    assert v == given


def test_get_options():
    options = '\n'.join([
        '# not included',
        '## not included',
        'included-1',
        '',
        ' included-2 ',
    ])
    result = takeit.get_options(options.encode('utf-8'))
    assert list(result) == [
        'included-1',
        'included-2',
    ]
