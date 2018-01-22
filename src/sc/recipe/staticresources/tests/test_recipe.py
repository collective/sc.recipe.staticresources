# -*- coding: utf-8 -*-
from sc.recipe.staticresources import Recipe
from shutil import rmtree
from tempfile import mkdtemp

import os
import unittest


class RecipeTestCase(unittest.TestCase):

    def setUp(self):
        test_dir = os.path.realpath(mkdtemp())
        for directory in ('bin', 'parts', 'eggs', 'develop-eggs'):
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
            options,
        )

    def test_minimal_options(self):
        static_resources = self._get_recipe(None, None, None)
        self.assertTrue(static_resources)
        self.assertIn('directory', static_resources.options)
        directory = '{0}/webpack'.format(self.test_dir)
        self.assertEqual(static_resources.options['directory'], directory)

    def test_custom_directory(self):
        options = self.options
        directory = '/tmp/webpack'
        options['directory'] = directory
        static_resources = self._get_recipe(None, None, options)
        self.assertEqual(static_resources.options['directory'], directory)
        static_resources.install()
        self.assertTrue(os.path.exists(directory))
        rmtree(directory)

    def test_custom_destination(self):
        options = self.options
        destination = '/tmp/static'
        options['destination'] = destination
        static_resources = self._get_recipe(None, None, options)
        self.assertEqual(static_resources.options['destination'], destination)
        self.static_resources.install()
        os.mkdir(destination)
        os.system('{0}/bin/build-mypackagename'.format(self.test_dir))
        self.assertTrue(os.path.exists(destination))
        rmtree(destination)

    def test_custom_bobtemplate(self):
        options = self.options
        bobtemplate = (
            'https://github.com/simplesconsultoria/sc.recipe.staticresources/'
            'archive/master.zip#sc.recipe.staticresources-master/src/sc/'
            'recipe/staticresources/bobtemplate'
        )
        options['bobtemplate'] = bobtemplate
        static_resources = self._get_recipe(None, None, options)
        self.assertEqual(static_resources.options['bobtemplate'], bobtemplate)
        static_resources.install()
        self.assertTrue(os.path.exists(options['directory']))

    def test_template_folder_being_created(self):
        self.static_resources.install()
        self.assertTrue(os.path.exists('{0}/webpack'.format(self.test_dir)))

    def test_remove_old_scritps(self):
        self.static_resources.install()
        self.assertTrue(os.path.exists('{0}/bin/build-mypackagename'.format(self.test_dir)))

        self.static_resources._remove_old_scritps()
        self.assertFalse(os.path.exists('{0}/bin/build-mypackagename'.format(self.test_dir)))
