# -*- coding: utf-8 -*-
import sys, os
from setuptools import setup
from setuptools.command.test import test as TestCommand

__version__='0.1.1'

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist bdist_wheel register upload")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (__version__,__version__))
    print("  git push --tags")
    sys.exit()

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

with open('README.md') as f:
  long_description = f.read()

setup(name='gsea_incontext_notk',
      version=__version__,
      description='GSEA-InContext Gene Set Enrichment Analysis in Python',
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 2.7',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Topic :: Software Development :: Libraries'],
      keywords= ['Gene Ontology', 'GO','Biology', 'Enrichment',
          'Bioinformatics', 'Computational Biology',],
      url='https://github.com/CostelloLab/GSEA-InContext_noTk',
      author='Rani Powers (fork originally from gsea_incontext_notk by Zhuoqing Fang)',
      author_email='rani.powers@cuanschutz.edu',
      license='MIT',
      packages=['gsea_incontext_notk'],
      install_requires=[
          'numpy>=1.13.0',
          'pandas>=0.16',
          'matplotlib>=1.4.3',
          'beautifulsoup4>=4.4.1',
          'requests',
          'scipy',],
      entry_points={'console_scripts': ['gsea_incontext_notk = gsea_incontext_notk.__main__:main'],},
      tests_require=['pytest'],
      cmdclass = {'test': PyTest},
      zip_safe=False,
      download_url='https://github.com/CostelloLab/GSEA-InContext_noTk',)

__author__ = 'Rani Powers'
