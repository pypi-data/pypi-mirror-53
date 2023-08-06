# murl

[![Documentation Status](https://readthedocs.org/projects/mrf-murl/badge/?version=latest)](http://mrf-murl.readthedocs.io/en/latest/?badge=latest)  [![Build Status](https://travis-ci.org/mariamrf/murl.svg?branch=master)](https://travis-ci.org/blaringsilence/murl) [![PyPI version](https://badge.fury.io/py/mrf-murl.svg)](https://badge.fury.io/py/mrf-murl)

A URI Manipulation module aimed at web use. Motivated by the **Quora challenge** (see note below), which is why `murl` has its own implementation of some functions in `urllib` and `urlparse`.

This README only has a very brief outline. Complete documentation can be found [here](http://mrf-murl.readthedocs.io).

**Note:** As of sometime between October 13th and October 29th, 2016, this challenge was removed from Quora. A copy of the prompt, however, can be found [in my blog post](https://blog.mariam.dev/2016/10/13/murl-init.html).

## URI Syntax
` scheme:[//[user:password@]host[:port]][/]path[?query][#fragment]`

Where:
  - Scheme must start with a letter followed by letters, digits, `+`, `.`, or `-` and then a colon.
  - Authority part which has username, password, host, and port has to start with a // and end with the end of the URI, a `/`, a `?`, or a `#`, whichever comes first.
  - Path must begin with `/` whenever there's an authority present. May begin with `/` if not, but never `//`.
  - Query must begin with `?` and is a string of any number of key=value pairs delimetered with `&` or `;` usually.
  - Keys in Query can be duplicates and indicate multiple values for the same thing.
  - Fragment must begin with `#` and span until the end of the URI.
  - All unsafe characters and unreserved characters in any given URI component must be percent-encoded in `% HEXDIG HEXDIG` format.
  - Domains (without subdomains, etc) must be `ONE_DOT_DELIMETERED_SEGMENT` + `.` + `PUBLIC_SUFFIX`, where `PUBLIC_SUFFIX` can have a number of dot-delimetered segments and a wide range of lengths/etc.

## General Use

- Install using pip: 
  ```bash 
  $ pip install mrf-murl
  ```

- Create a `Murl` object using an existing relative or absolute but valid/standard URI or without any parameters to construct the URI dynamically.
- Add/change/get URI components:
  - scheme [add/change/get]
  - host (entire string, including subdomains, etc, but not port) [add/change/get]
  - domain (only the domain without any subdomains, etc) [get]
  - auth (username/password) [add/change/get]
  - port [add/change/get]
  - path [add/change/get]
  - query string/individual key/value pairs [add/change/get]
  - fragment [add/change/get]
  
## References

- [RFC 3986 (2005)](https://tools.ietf.org/html/rfc3986)
- [Public Suffix List](https://publicsuffix.org/)
