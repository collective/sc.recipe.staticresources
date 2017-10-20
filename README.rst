*************************
sc.recipe.staticresources
*************************

.. contents:: Table of Contents

Life, the Universe, and Everything
----------------------------------

This package is used as a recipe to integrate Plone and Webpack using buildout.

Mostly Harmless
---------------

.. image:: http://img.shields.io/pypi/v/sc.recipe.staticresources.svg
   :target: https://pypi.python.org/pypi/sc.recipe.staticresources

.. image:: https://img.shields.io/travis/simplesconsultoria/sc.recipe.staticresources/master.svg
    :target: http://travis-ci.org/simplesconsultoria/sc.recipe.staticresources

.. image:: https://img.shields.io/coveralls/simplesconsultoria/sc.recipe.staticresources/master.svg
    :target: https://coveralls.io/r/simplesconsultoria/sc.recipe.staticresources

Got an idea? Found a bug? Let us know by `opening a support ticket <https://github.com/simplesconsultoria/sc.recipe.staticresources/issues>`_.

Don't Panic
-----------

Installation
^^^^^^^^^^^^

To enable this product in a buildout-based installation:

#. Edit your buildout.cfg and add these lines::

    [buildout]
    ...
    parts +=
        webpack
        staticresources

    [webpack]
    recipe = gp.recipe.node
    version = 6.6.0
    npms = npm yarn webpack@2
    scripts = npm yarn webpack

    [staticresources]
    recipe = sc.recipe.staticresources
    name = my.package.name
    short_name = mypackagename

    # Relative path to webpack folder
    # If this option is not present, the default value is ${buildout:directory}/webpack
    directory = src/my.package.name/webpack

    # Destination path relative to webpack directory
    # If this option is not present, the default value is ${buildout:directory}/webpack/dist
    destination = ../src/my/package/name/static

    # Custom webpack bobtemplate path
    # If this option is not present, the default value is the bobtemplate that exists into this package
    bobtemplate = bobtemplate

After updating the configuration you need to run ''bin/buildout'', which will take care of updating your system.

The recipe is responsible to:

a. Create webpack folder structure, if not exists
b. Create one script to access webpack environment to handle more complex scenarios.
c. Create all scripts listed in webpack/package.json scripts entries.

Usage
^^^^^

In our simplest example, those scripts are created:

.. code-block:: bash

    $ bin/env-mypackagename

This command set the buildout node installation in the system PATH, this way you can use Webpack as described on Webpack docs.

.. code-block:: bash

    $ bin/watch-mypackagename

This command makes Webpack wait for any change in any LESS, JS (ES6) files and generate the minified version of CSS and JS (ES5) UMD module for your application.

.. code-block:: bash

    $ bin/dev-mypackagename

This does the same as watch command, but don't try to minify the final CSS and JS.  Used for debug purpose.

.. code-block:: bash

    $ bin/build-mypackagename

This command build the CSS and JS minified, but don't wait for any change.

Note that the short_name is added in the end of the script, this way you can have multiple webpack folders in the same package (if you have multiple themes inside the same package for example).
