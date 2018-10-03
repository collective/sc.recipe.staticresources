*************************
sc.recipe.staticresources
*************************

.. contents:: Table of Contents

Life, the Universe, and Everything
==================================

This Buildout recipe is used to integrate Plone and `webpack <https://webpack.js.org/>`_.

In recent years, many tools were created to manage static resource files, these tools can:

* automatically compress images
* use CSS pre and post-processors to write less and better code, taking advantage of new standards still not available to all browsers
* use JavaScript transpilers to write ES6 code and generate ES5 equivalent code, that works on all browsers
* minify the resulting code

And many other options, practically everything related to process static resources can be achived by an official or community package.

This recipe let's you write less lines into your Buildout configuration and provides a nice template to start with.

We choose `webpack`_ because it's proven to be the best toolchain available, and many people in the Plone community are already using it.

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
        node
        staticresources

    [node]
    recipe = gp.recipe.node
    version = 8.11.2
    npms = npm yarn
    scripts = npm yarn

    [staticresources]
    recipe = sc.recipe.staticresources
    name = my.package
    short_name = mypackage

After updating the configuration you need to run ''bin/buildout'', which will take care of updating your system.

The recipe is responsible for:

* creating the `webpack`_ folder structure, if none exists
* creating the script to access `webpack`_ environment to handle more complex scenarios
* create all scripts listed in ``webpack/package.json`` scripts entries.

Configuration options
---------------------

name (required)
^^^^^^^^^^^^^^^
This is the package name or the theme name used in the package.
This field is required.

short_name (required)
^^^^^^^^^^^^^^^^^^^^^
A short name is needed to be used as the UMD JavaScript library name and the name of the script inserted into Plone.
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
Custom webpack bobtemplate path.
It's possible to change the default bobtemplate path to another that follows your project needs, if you prefer.
If this option is not present, the default value is the bobtemplate that exists into this package.

The default template
--------------------
In the default template we selected what webpack tools are valid to our needs, what is basically theme and addons development.
This is the list of what we include:

`HTML Loader <https://github.com/webpack-contrib/html-loader>`_
    Used to process the HTML file; in our use case it's used when we create a new theme.

`Image Webpack Loader <https://github.com/tcoopman/image-webpack-loader>`_
    Process all images referenced to save space in the final images,
    it tile the workflow with some specialized tools for each image format.

`SVG URL Loader <https://github.com/bhovhannes/svg-url-loader>`_
    Process all SVG files and creates a data-url string.
    For example it inserts the SVG file into the final CSS file to save requests.

`Webpack SpriteSmith <https://github.com/mixtur/webpack-spritesmith>`_
    Brings an easy way to create image sprites,
    you simply add the icon images in one folder and it creates all you need to use the sprite with your choosen CSS pre-processor.

`Babel <https://babeljs.io/>`_
    A transpiler that makes possible to use the next generation of JavaScript today.

`Sass <http://sass-lang.com/>`_
    The most mature, stable, and powerful professional grade CSS extension language in the world.

`PostCSS <https://github.com/postcss/postcss>`_
    A post-processor used to transform styles with JavaScript plugins.
    In our configuration we use just `CSS next <http://cssnext.io/>`_ plugin to add automatically all vendor prefixes for the last 3 versions of major browsers,
    as soon as the browsers support more features,
    your final CSS will automatically cost less bytes.

JavaScript Helper
-----------------
There's a little helper created to simplify the configuration burden of add-ons that use this recipe.
Let's see how to use it:

1. Create a ``package.json`` file with the following:

.. code-block:: json

    {
      "name": "my.package",
      "version": "0.0.1",
      "main": "app/mypackage.js",
      "scripts": {
        "build": "./node_modules/.bin/webpack -p",
        "debug": "NODE_ENV=debug ./node_modules/.bin/webpack --watch",
        "watch": "./node_modules/.bin/webpack -p --watch",
        "test": "NODE_ENV=testing ./node_modules/.bin/karma start --single-run"
      },
      "repository": {},
      "license": "GPL-2.0",
      "dependencies": {
        "sc-recipe-staticresources": "simplesconsultoria/sc.recipe.staticresources#1.1b2"
      }
    }

This way it's possible to add all dependencies of the configuration with just one line,
keeping versions well tested across all ecosystems just like Buildout's versions do.

2. Create a ``webpack.config.js`` file with the following:

.. code-block:: javascript

   const makeConfig = require('sc-recipe-staticresources');
   const CopyWebpackPlugin = require('copy-webpack-plugin');

   module.exports = makeConfig(
     // name
     'my.package',

     // shortName
     'mypackage',

     // path
     `${__dirname}/dist`,

     //publicPath
     `${__dirname}/../src/my/package/browser/static`,

     //callback
     function(config, options) {
       config.entry.unshift(
         './app/img/img1.png',
         './app/img/img2.png',
         './app/img/img3.png',
       );
       config.plugins.push(
         new CopyWebpackPlugin([{
           from: 'app/folder/*',
           to: 'folder',
           flatten: true
         }]),
       );
       
     },
   );

This way it's possible to inherit a configuration of all dependencies in the current version.

Our mrbob template generates this configuration when the recipe is run for the first time.
You can modify it to fit your needs,
but for most themes and add-ons these defaults are a good starting point (something similar to Buildout's extend configuration).

Usage
-----

In our simplest example, the following scripts are created:

.. code-block:: console

    $ bin/env-mypackage

This command sets the buildout node installation in the system PATH, this way you can use webpack as described in their docs.

.. code-block:: console

    $ bin/watch-mypackage

This command makes webpack wait for any change in any SASS, JS (ES6) files and generates the minified version of CSS and JS (ES5) UMD module for your application.

.. code-block:: console

    $ bin/debug-mypackage

This does the same as watch command, but don't try to minify the final CSS and JS.
Used for debug purposes.

.. code-block:: console

    $ bin/build-mypackage

This command builds the CSS and JS minified, but doesn't wait for any change.

.. code-block:: console

    $ bin/test-mypackage

This command runs the JavaScript tests using `karma <https://karma-runner.github.io>`_, `mocha <https://mochajs.org/>`_, `chai <http://chaijs.com/>`_ and `sinon <http://sinonjs.org/>`_.

Note that ``short_name`` is added at the end of the script name.
This way you can have multiple webpack folders in the same package (if you have multiple themes inside the same package, for example).
