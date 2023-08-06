convenience functions for working with URLs


*Latest release 20191004*:
Small updates for changes to other modules.



## Function `isURL(U)`

Test if an object `U` is an URL instance.

## Class `NetrcHTTPPasswordMgr`

MRO: `urllib.request.HTTPPasswordMgrWithDefaultRealm`, `urllib.request.HTTPPasswordMgr`  
A subclass of HTTPPasswordMgrWithDefaultRealm that consults
the .netrc file if no overriding credentials have been stored.

## Function `skip_errs(iterable)`

Iterate over `iterable` and yield its values.
If it raises URLError or HTTPError, report the error and skip the result.

## Function `strip_whitespace(s)`

Strip whitespace characters from a string, per HTML 4.01 section 1.6 and appendix E.

## Function `URL(U, referer, **kw)`

Factory function to return a _URL object from a URL string.
Handing it a _URL object returns the object.



# Release Log

*Release 20191004*:
Small updates for changes to other modules.

*Release 20160828*:
Use "install_requires" instead of "requires" in DISTINFO.

*Release 20160827*:
Handle TimeoutError, reporting elapsed time.
URL: present ._fetch as .GET.
URL: add .resolve to resolve this URL against a base URL.
URL: add .savepath and .unsavepath methods to generate nonconflicting save pathnames for URLs and the reverse.
URL._fetch: record the post-redirection URL as final_url.
New URLLimit class for specifying simple tests for URL acceptance.
New walk(): method to walk website from starting URL, yielding URLs.
URL.content_length property, returns int or None if header missing.
New URL.normalised method to return URL with . and .. processed in the path.
new URL.exists test function.
Assorted bugfixes and improvements.

*Release 20150116*:
Initial PyPI release.
