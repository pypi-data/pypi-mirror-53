# [Changelog](https://keepachangelog.com)

## v0.4.5 :: 20191007

- db6ac6d Go back to using cryptography due to
  https://www.cvedetails.com/cve/CVE-2013-7459/
- c70ad51 Allow users to override password (thanks @alairock)

## v0.4.4 :: 20180706

- Optionally outputs cookies to a file compatible with cURL (thanks to
  Muntashir Al-Islam!)

## v0.4.3 :: 20170627

- Consistently use Chrome as default across platforms, allow user to specify
  Chromium as desired (thanks @jtbraun)

## v0.4.0 :: 20170504

- Remove compatibility for Python <3.5
- Add type hints
- Refactor for smaller functions
- Expand docstrings
- Revert from `cryptography` back to `PyCrypto` and `hashlib` for easier
  installation.

## v0.3.4 :: 20170414

- Add support for new Ubuntu keyring / libsecret
  - See <https://github.com/n8henrie/pycookiecheat/issues/12> for details
  - Many thanks to @stat1c1c3au and @trideceth12 for contributions

## 0.3.0

- Use [`cryptography`](https://cryptography.io/en/latest/) instead of
  `pycrypto` (thanks to [Taik](https://github.com/Taik)!)
  - Seems to be [significantly
    faster](https://github.com/n8henrie/pycookiecheat/pull/11#issuecomment-221950400)
  - Works with PyPy >= 2.6.0 (no support for PyPy3 yet)

## 0.2.0

- Fix domain and subdomain matching
- Make SQL query more secure by avoiding string formatting
- Many thanks to [Brandon Rhodes](https://github.com/brandon-rhodes) for 24c4234 !

## 0.1.10

- Read version to separate file so it can be imported in setup.py
- Bugfix for python2 on linux

## 0.1.9

- Bugfix for python2 on linux

## 0.1.8

- Python2 support (thanks [dani14-96](https://github.com/dani14-96))

## 0.1.7

- Configurable cookies file (thanks [ankostis](https://github.com/ankostis))

## 0.1.6

- OSError instead of Exception for wrong OS.
- Moved testing requirements to tox and travis-ci files.

## 0.1.5

- Updated to work better with PyPI's lack of markdown support
- Working on tox and travis-ci integration
- Added a few basic tests that should pass if one has Chrome installed and has visited my site (n8henrie.com)
- Added sys.exit(0) if cookie_file not found so tests pass on travis-ci.

## 0.1.0 (2015-02-25)

- First release on PyPI.

## Prior changelog from Gist

- 20150221 v2.0.1: Now should find cookies for base domain and all subs.
- 20140518 v2.0: Now works with Chrome's new encrypted cookies.
