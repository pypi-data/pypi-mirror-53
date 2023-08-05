from setuptools import setup
from setuptools import find_packages
import sys
import os
from codecs import open

here = os.path.abspath(os.path.dirname(__file__))

if sys.argv[-1]:
    if sys.argv[-1] == 'publish':
        os.system('python setup.py sdist bdist_wheel')
        os.system('twine upload dist/*')
        sys.exit()
    elif sys.argv[-1] == 'uninstall':
        os.system('rm -rf build')
        os.system('rm -rf dist')
        os.system('rm -rf spyraio.egg-info')

        sys.exit()

requires = [
    'numpy',
    'matplotlib'
]

ABOUT = {}
with open(os.path.join(here, 'spyraio', '__about__.py'), 'r', 'utf-8') as f:
    exec(f.read(), ABOUT)

setup(
    name=ABOUT['__title__'],
    version=ABOUT['__version__'],
    url=ABOUT['__url__'],
    license=ABOUT['__license__'],
    author=ABOUT['__author__'],
    author_email=ABOUT['__author_email__'],
    keywords=ABOUT['__keywords__'],
    description=ABOUT['__description__'],
#    packages=['spyraio'],
    install_requires=requires,
    packages=find_packages())