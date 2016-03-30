import sys

if sys.version_info[0] == 3:
    to_b = lambda a: a.encode('utf-8')
    to_s = lambda a: a.decode('utf-8')
else:
    to_b = str
    to_s = unicode
