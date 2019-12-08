
from setuptools import setup, find_packages
from lars.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='ulars',
    version=VERSION,
    description='From txt to sqlite3 parser of logs',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Camille Galladjov',
    author_email='ujinjinjin@outlook.com',
    url='https://github.com/Ujinjinjin/lars',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'lars': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        lars = lars.main:main
    """,
)
