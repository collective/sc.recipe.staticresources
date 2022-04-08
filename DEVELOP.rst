Using the development buildout
==============================

Install
-------

Create a virtualenv in the package::

    $ virtualenv -p python2 .

Install requirements with pip::

    $ ./bin/pip install -r requirements.txt

Run buildout::

    $ ./bin/buildout


Running tests
-------------

    $ tox

list all tox environments::

    $ tox -l
    py27
    code-analysis
    lint
    coverage-report

run a specific tox env::

    $ tox -e py27


CI Github-Actions / codecov
---------------------------

The first time you push the repo to github, you might get an error from codecov.
Either you activate the package here: `https://app.codecov.io/gh/collective/+ <https://app.codecov.io/gh/collective/+>`_
Or you just wait a bit, codecov will activate your package automatically.
