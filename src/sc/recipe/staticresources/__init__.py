# -*- coding: utf-8 -*-
from mrbob.configurator import parse_template
from mrbob.rendering import jinja2_renderer
from mrbob.rendering import render_structure
from os import path
from zc.buildout import UserError

import json
import logging
import os
import subprocess


CURRENT_DIR = path.dirname(__file__)
SCRIPT_TEMPLATE = """#!/bin/sh
export PATH={bin_directory}:$PATH
cd {webpack_directory}
yarn
{command}"""


class Recipe(object):

    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        self.logger = logging.getLogger(self.name)
        self.bin_directory = buildout['buildout']['bin-directory']

        # Check required options
        if not self.options.get('name', False):
            self._error('Missing "name" parameter with the package name.')
        if not self.options.get('short_name', False):
            self._error('Missing "short_name" parameter with a simplified name of package.')
        self.short_name = options['short_name']

        # Set default value for options
        directory = self.buildout['buildout']['directory']
        self.options.setdefault('directory', '{0}/webpack'.format(directory))
        self.webpack_directory = options['directory']
        self.options.setdefault('destination', 'dist')
        self.options.setdefault('bobtemplate', path.join(CURRENT_DIR, 'bobtemplate'))
        self.bobtemplate = options['bobtemplate']

    def _error(self, msg):
        self.logger.error(msg)
        raise UserError(msg)

    def _run_mrbob(self):
        template = parse_template(self.bobtemplate)[0]
        output_dir = self.webpack_directory
        variables = self.options
        verbose = True
        renderer = jinja2_renderer
        ignored_files = []
        ignored_directories = []

        os.mkdir(output_dir)
        render_structure(
            template,
            output_dir,
            variables,
            verbose,
            renderer,
            ignored_files,
            ignored_directories,
        )

    def _create_script(self, name, command):
        script_name = name + '-' + self.short_name
        out_file = self.bin_directory + '/' + script_name
        with open(out_file, 'w') as output:
            data = SCRIPT_TEMPLATE.format(
                bin_directory=self.bin_directory,
                webpack_directory=self.webpack_directory,
                command=command
            )
            output.write(data)
        subprocess.call(['chmod', '775', out_file])
        self.logger.info('Install ' + script_name)

    def install(self):
        if not path.isdir(self.webpack_directory):
            self._run_mrbob()

        with open(self.webpack_directory + '/package.json') as data_file:
            package_json = json.load(data_file)

        for name in package_json['scripts']:
            self._create_script(name, 'npm run ' + name)

        self._create_script('env', '/bin/bash')

    def update(self):
        self.install()
