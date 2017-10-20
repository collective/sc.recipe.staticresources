# -*- coding: utf-8 -*-
from sc.recipe.staticresources import Recipe
from shutil import rmtree
from tempfile import mkdtemp
from testfixtures import OutputCapture

import os
import unittest


class RecipeTestCase(unittest.TestCase):

    def setUp(self):
        test_dir = os.path.realpath(mkdtemp())
        for directory in ('bin', 'parts', 'eggs', 'develop-eggs', ):
            os.makedirs('{0}/{1}'.format(test_dir, directory))

        self.buildout_options = {
            'buildout': {
                'bin-directory': '{0}/bin'.format(test_dir),
                'parts-directory': '{0}/parts'.format(test_dir),
                'python': 'buildout',
                'executable': '{0}/bin/python2.7'.format(test_dir),
                'directory': '{0}'.format(test_dir),
                'find-links': '',
                'allow-hosts': '*',
                'eggs-directory': '{0}/eggs'.format(test_dir),
                'develop-eggs-directory': '{0}/develop-eggs'.format(test_dir),
            },
        }
        self.test_dir = test_dir
        self.options = {
            'recipe': 'sc.recipe.staticresources',
            'name': 'my.package.name',
            'short_name': 'mypackagename',
        }
        self.name = 'static-resources'
        self.static_resources = self._get_recipe()

    def tearDown(self):  # noqa
        rmtree(self.test_dir)

    def _get_recipe(self, buildout_options=None, name=None, options=None):
        if buildout_options is None:
            buildout_options = self.buildout_options
        if name is None:
            name = self.name
        if options is None:
            options = self.options
        return Recipe(
            buildout_options,
            name,
            options
        )

    def test_minimal_options(self):
        static_resources = self._get_recipe(None, None, None)
        self.assertTrue(static_resources)
        self.assertIn('directory', static_resources.options)
        directory = '{0}/webpack'.format(self.test_dir)
        self.assertEqual(static_resources.options['directory'], directory)

    def test_custom_directory(self):
        options = self.options
        directory = '/opt/recipe/webpack'
        options['directory'] = directory
        static_resources = self._get_recipe(None, None, options)
        self.assertEqual(static_resources.options['directory'], directory)

    def test_hooks_folder_being_created(self):
        with OutputCapture() as out:  # noqa F841
            self.static_resources.install()
            # out.compare('Install Git pre-commit hook.')
        self.assertTrue(os.path.exists('{0}/webpack'.format(self.test_dir)))

    # def test_egg(self):
    #     self.assertTrue(self.static_resources.egg)

    # def test_location(self):
    #     location = '{0}/{1}'.format(
    #         self.buildout_options['buildout']['parts-directory'],
    #         self.name
    #     )
    #     self.assertEqual(
    #         self.static_resources.options['location'],
    #         location
    #     )

    # def test_extensions_default(self):
    #     self.assertEqual(
    #         self.static_resources.extensions,
    #         ['flake8>=2.0.0', ]
    #     )

    # def test_extensions_no_flake8(self):
    #     self.options['flake8'] = False
    #     self.static_resources = self._get_recipe()
    #     self.assertEqual(self.static_resources.extensions, [])

    # def test_extensions_flake8_plugins(self):
    #     self.options['flake8-extensions'] = 'pep8-naming\nflake8-todo'
    #     self.static_resources = self._get_recipe()
    #     self.assertEqual(
    #         self.static_resources.extensions,
    #         ['flake8>=2.0.0', 'pep8-naming', 'flake8-todo']
    #     )

    # def test_extensions_flake8_empty_plugins(self):
    #     self.options['flake8-extensions'] = '\n\n'
    #     self.static_resources = self._get_recipe()
    #     self.assertEqual(
    #         self.static_resources.extensions,
    #         ['flake8>=2.0.0', ]
    #     )