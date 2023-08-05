from setuptools import setup

about = {}
with open('pyprofilers/__about__.py') as file:
    exec(file.read(), about)

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    url=about['__url__'],
    author=about['__author__'],
    license=about['__license__'],
    packages=['pyprofilers'],

    install_requires=['line_profiler', 'yappi']
)
