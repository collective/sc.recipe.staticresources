# -*- coding: utf-8 -*-
"""Installer for the sc.recipe.staticresources package."""

from setuptools import find_packages, setup

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])

entry_point = 'sc.recipe.staticresources:Recipe'
entry_points = {
    'zc.buildout': [
        'default = {0:s}'.format(entry_point)
    ]
}


setup(
    name='sc.recipe.staticresources',
    version='1.1b8.dev0',
    description="Buildout recipe to integrate Plone and webpack",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
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
    keywords='Python buildout recipe',
    author='Simples Consultoria',
    author_email='products@simplesconsultoria.com.br',
    url='https://github.com/collective/sc.recipe.staticresources',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/sc.recipe.staticresources',
        'Source': 'https://github.com/collective/sc.recipe.staticresources',
        'Tracker': 'https://github.com/collective/sc.recipe.staticresources/issues',
        # 'Documentation': 'https://sc.recipe.staticresources.readthedocs.io/en/latest/',
    },
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['sc', 'sc.recipe'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=2.7",
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
