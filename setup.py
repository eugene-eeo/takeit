from setuptools import setup

setup(
    name='takeit',
    version='0.1.0',
    description='quickly steal files from cdnjs',
    url='https://github.com/eugene-eeo/takeit',
    author='Eeo Jun',
    author_email='packwolf58@gmail.com',
    license='MIT',
    packages=['takeit'],
    install_requires=[
        'requests==2.9.1',
        'python-editor==1.0',
        'docopt==0.6.2',
        'bs4==0.0.1',
        'uritemplate.py==0.3.0',
    ],
    entry_points='''
        [console_scripts]
        takeit=takeit.cmd:main
    ''',
    tests_require=[
        'pytest',
    ],
)
