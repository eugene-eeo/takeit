takeit
======

    "Awake! Avast! Hold tight your buns, if buns you do hold
    dear. For time has come to wake and run and not give way
    to fear!"

    -- Earl of Lemongrab

A script downloader for quick and dirty front-end prototyping.
No, really. All it does is look up the library on cdnjs, does
some scraping and then downloads the files for you. Usage::

    $ takeit jquery lodash.js==4.6.1
    $ takeit --html jquery
    $ takeit --html jquery > index.html

*Take it away* (to the dungeon).

Install
-------

Currently the only way to install it is to clone the repo and
then do a pip-install. It will add a ``takeit`` binary to
somewhere in your PATH::

    $ git clone git@github.com:eugene-eeo/takeit.git
    $ cd takeit && pip install .
