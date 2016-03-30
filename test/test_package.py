from takeit.package import Package


def test_url():
    given = Package('tw', '1.2.0').url
    assert given == 'https://cdnjs.com/libraries/tw/1.2.0'


def test_from_string():
    pkg = Package.from_string('tw==1.2.0')
    assert pkg.id == 'tw'
    assert pkg.version == '1.2.0'


def test_from_string_ambiguous():
    pkg = Package.from_string('tw==123==one')
    assert pkg.id == 'tw==123'
    assert pkg.version == 'one'
