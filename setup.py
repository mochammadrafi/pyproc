import re

from setuptools import setup, find_packages
from os import path


BASE_DIR = path.abspath(path.dirname(__file__))

with open(path.join(BASE_DIR, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def get_version():
    filename = path.join('pyproc', '__init__.py')

    with open(filename, 'r') as f:
        content = f.read()

    version = re.findall(r"version[\s+='_\"]+(.*)['\"]", content)

    return version[0]

setup(
    name='pyproc',
    version=get_version(),
    description='Python SPSEv4 wrapper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/mochammadrafi/pyproc',
    author='Agung Pratama',
    author_email='agungpratama1001@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Natural Language :: English',
        'Natural Language :: Indonesian',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.7',
    install_requires=[
        'requests',
        'BeautifulSoup4',
        'html5lib',
        'backoff',
    ],
    entry_points={
        'console_scripts': ['pyproc=scripts.downloader:main']
    },
    project_urls={
        'Bug Reports': 'https://gitlab.com/mochammadrafi/pyproc/issues',
        'Source': 'https://gitlab.com/mochammadrafi/pyproc'
    },
    keywords='api, spse, lpse, pengadaan, procurement, lkpp, lelang, tender',
    packages=find_packages(exclude=['tests', 'examples']),
    zip_safe=True,
    license='MIT'
)
