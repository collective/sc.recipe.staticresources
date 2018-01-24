# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '1.0a2'
description = 'FIXME'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

entry_point = 'sc.recipe.staticresources:Recipe'
entry_points = {
    'zc.buildout': [
        'default = {0:s}'.format(entry_point)
    ]
}

setup(name='sc.recipe.staticresources',
      version=version,
      description=description,
      long_description=long_description,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Framework :: Buildout',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python',
          'Topic :: Software Development :: Build Tools',
      ],
      keywords='',
      author='Simples Consultoria',
      author_email='products@simplesconsultoria.com.br',
      url='http://github.com/simplesconsultoria/sc.recipe.staticresources/',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['sc', 'sc.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'mr.bob',
          'setuptools',
          'zc.buildout',
          'zc.recipe.egg',
      ],
      extras_require={
          'test': [
              'testfixtures',
              'zc.buildout [test]',
              'zope.testing',
          ],
      },
      entry_points=entry_points,
      )
