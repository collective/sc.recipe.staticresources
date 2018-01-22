*************************
sc.recipe.staticresources
*************************

.. contents:: Table of Contents

Life, the Universe, and Everything
==================================

This package is used as a recipe to integrate Plone and Webpack using buildout.

In the recent years, many tools were created to manage static resource files, these tools can:

* Automatically compress images.
* Use CSS Pre-processors and Post-processors to write less and better code, taking advantage of new standards still not available to all browsers.
* Use Javascript transpiller to write ES6 code and generate ES5 equivalent code, that work on all browsers.
* Minify resulting code.
* And many other options, pratically everything related to process static resources can be achived by an official or community package.

This package has the dutty to facilitates the integration of Webpack with Plone,
writing less lines into your buildout configuration and provide a nice template to start with.

We choose Webpack because it is proven to be the best toolchain available, and many people in the Plone Community are using it.

Mostly Harmless
===============

.. image:: http://img.shields.io/pypi/v/sc.recipe.staticresources.svg
   :target: https://pypi.python.org/pypi/sc.recipe.staticresources

.. image:: https://img.shields.io/travis/simplesconsultoria/sc.recipe.staticresources/master.svg
    :target: http://travis-ci.org/simplesconsultoria/sc.recipe.staticresources

.. image:: https://img.shields.io/coveralls/simplesconsultoria/sc.recipe.staticresources/master.svg
    :target: https://coveralls.io/r/simplesconsultoria/sc.recipe.staticresources

Got an idea? Found a bug? Let us know by `opening a support ticket <https://github.com/simplesconsultoria/sc.recipe.staticresources/issues>`_.

Don't Panic
===========

Installation


To enable this product in a buildout-based installation:

#. Edit your buildout.cfg and add these lines:

.. code-block:: ini

    [buildout]
    ...
    parts +=
        webpack
        staticresources

    [webpack]
    recipe = gp.recipe.node
    version = 6.6.0
    npms = npm yarn
    scripts = npm yarn

    [staticresources]
    recipe = sc.recipe.staticresources
    name = my.package.name
    short_name = mypackagename

After updating the configuration you need to run ''bin/buildout'', which will take care of updating your system.

The recipe is responsible to:

a. Create webpack folder structure, if not exists
b. Create one script to access webpack environment to handle more complex scenarios.
c. Create all scripts listed in webpack/package.json scripts entries.

Configuration Options
---------------------

name (required)
^^^^^^^^^^^^^^^
This is the package name or the theme name used in the package.
This field is required.

short_name (required)
^^^^^^^^^^^^^^^^^^^^^
A short name is needed to be used as the UMD Javascript library name and the name of the script inserted into Plone.
This field is required.

directory
^^^^^^^^^
Relative path to webpack folder, you can use this field to define more than one webpack folder for different themes.
If this option is not present, the default value is ``${buildout:directory}/webpack``.

destination
^^^^^^^^^^^
Destination path relative to webpack directory, you should add this option to point the resulting static resources folder,
it can be the theme folder or a static resources directory.
If this option is not present, the default value is ``./dist`` folder.

bobtemplate
^^^^^^^^^^^
Custom webpack bobtemplate path, if you prefer, it is possible to change the default bobtemplate to another to follow your project needs.
If this option is not present, the default value is the bobtemplate that exists into this package.

The default template
--------------------
In the default template we selected what Webpack tools are valid to our needs, what is basically Theme and addons development.
This is the list of what we include:

HTML Loader
^^^^^^^^^^^
`HTML Loader <https://github.com/webpack-contrib/html-loader>`_ is used to process the HTML file in our use case we use it when create a new theme.

Image Webpack Loader
^^^^^^^^^^^^^^^^^^^^
`Image Webpack Loader <https://github.com/tcoopman/image-webpack-loader>`_ process all images referenced to save space in the final images,
it tile the workflow with some specialized tools for each image format.

SVG URL Loader
^^^^^^^^^^^^^^
`SVG URL Loader <https://github.com/bhovhannes/svg-url-loader>`_ process all SVG files and create a data-url string.
For example it inserts the SVG file into the final CSS file to save requests.

Webpack SpriteSmith
^^^^^^^^^^^^^^^^^^^
`Webpack SpriteSmith <https://github.com/mixtur/webpack-spritesmith>`_ brings an easy way to create image sprites,
you simply add the icon images in one folder and it creates all you need to use the sprite with your choosen CSS pre-processor.

Babel transpiller
^^^^^^^^^^^^^^^^^
`Babel <https://babeljs.io/>`_ makes possible to use the next generation of Javascript today.

Sass
^^^^
`Sass <http://sass-lang.com/>`_ is the most mature, stable, and powerful professional grade CSS extension language in the world.

PostCSS
^^^^^^^
`PostCSS <https://github.com/postcss/postcss>`_ is a post-processor used to transform styles with JS plugins.
In our configuration we use just `CSS next <http://cssnext.io/>`_ plugin to add automatically all vendor prefixes for the last 3 versions of major browsers,
what means that acordding the browsers support more features,
your final CSS will automatically cost less bytes.

Usage
-----

In our simplest example, those scripts are created:

.. code-block:: console

    $ bin/env-mypackagename

This command set the buildout node installation in the system PATH, this way you can use Webpack as described on Webpack docs.

.. code-block:: console

    $ bin/watch-mypackagename

This command makes Webpack wait for any change in any SASS, JS (ES6) files and generate the minified version of CSS and JS (ES5) UMD module for your application.

.. code-block:: console

    $ bin/debug-mypackagename

This does the same as watch command, but don't try to minify the final CSS and JS.  Used for debug purpose.

.. code-block:: console

    $ bin/build-mypackagename

This command build the CSS and JS minified, but don't wait for any change.

.. code-block:: console

    $ bin/test-mypackagename

This command run the JS tests using `karma <https://karma-runner.github.io>`_, `mocha <https://mochajs.org/>`_, `chai <http://chaijs.com/>`_ and `sinon <http://sinonjs.org/>`_.

Note that the short_name is added in the end of the script, this way you can have multiple webpack folders in the same package (if you have multiple themes inside the same package for example).
