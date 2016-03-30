from setuptools import setup

setup(
    name='takeit',
    version='0.1.0',
    py_modules=['takeit'],
    install_requires=[
        'requests==2.9.1',
        'python-editor==0.4',
        'docopt==0.6.2',
        'bs4==0.0.1',
        'uritemplate.py==0.3.0',
    ],
    entry_points='''
        [console_scripts]
        takeit=takeit:main
    '''
)
