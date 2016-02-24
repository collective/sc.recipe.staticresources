# -*- coding: utf-8 -*-
from os import listdir
from os import path

import subprocess


current_dir = path.dirname(__file__)


class Recipe(object):

    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options

        # set required default options
        self.options.setdefault('option1', '.')
        self.options.setdefault('option2', 'False')
        self.options.setdefault('option3', 'True')

    def install(self):
        bin_directory = self.buildout['buildout']['bin-directory']
        scripts = [
            f for f in listdir(current_dir)
            if path.isfile(path.join(current_dir, f))
        ]

        for s in scripts:
            with open(bin_directory + '/script', 'w') as output_file:
                output_file.write('#!/bin/bash\nbin/code-analysis')
            subprocess.call(['chmod', '775', bin_directory + '/' + s])
            print('Install ' + s)

    def update(self):
        self.install()
