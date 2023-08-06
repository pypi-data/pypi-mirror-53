#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.urlutils',
  description = 'convenience functions for working with URLs',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20191004',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
  include_package_data = True,
  install_requires = ['lxml', 'beautifulsoup4', 'cs.excutils', 'cs.lex', 'cs.logutils', 'cs.rfc2616', 'cs.threads', 'cs.py3', 'cs.obj'],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 or later (GPLv3+)',
  long_description = '*Latest release 20191004*:\nSmall updates for changes to other modules.\n\n\n\n## Function `isURL(U)`\n\nTest if an object `U` is an URL instance.\n\n## Class `NetrcHTTPPasswordMgr`\n\nMRO: `urllib.request.HTTPPasswordMgrWithDefaultRealm`, `urllib.request.HTTPPasswordMgr`  \nA subclass of HTTPPasswordMgrWithDefaultRealm that consults\nthe .netrc file if no overriding credentials have been stored.\n\n## Function `skip_errs(iterable)`\n\nIterate over `iterable` and yield its values.\nIf it raises URLError or HTTPError, report the error and skip the result.\n\n## Function `strip_whitespace(s)`\n\nStrip whitespace characters from a string, per HTML 4.01 section 1.6 and appendix E.\n\n## Function `URL(U, referer, **kw)`\n\nFactory function to return a _URL object from a URL string.\nHanding it a _URL object returns the object.\n\n\n\n# Release Log\n\n*Release 20191004*:\nSmall updates for changes to other modules.\n\n*Release 20160828*:\nUse "install_requires" instead of "requires" in DISTINFO.\n\n*Release 20160827*:\nHandle TimeoutError, reporting elapsed time.\nURL: present ._fetch as .GET.\nURL: add .resolve to resolve this URL against a base URL.\nURL: add .savepath and .unsavepath methods to generate nonconflicting save pathnames for URLs and the reverse.\nURL._fetch: record the post-redirection URL as final_url.\nNew URLLimit class for specifying simple tests for URL acceptance.\nNew walk(): method to walk website from starting URL, yielding URLs.\nURL.content_length property, returns int or None if header missing.\nNew URL.normalised method to return URL with . and .. processed in the path.\nnew URL.exists test function.\nAssorted bugfixes and improvements.\n\n*Release 20150116*:\nInitial PyPI release.',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.urlutils'],
)
