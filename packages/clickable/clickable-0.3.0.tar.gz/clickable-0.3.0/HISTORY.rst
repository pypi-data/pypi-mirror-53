=======
History
=======

0.3.0 (2018-12)
---------------

* remove clickable.bootstrap module
* clickable.click use 'main' as default function when searching
  an entry-point in clickables.py
* tasks.py renamed to clickables.yml
* added an helper to load base configuration from clickables.yml
  (clickables.utils.load_config)
* python3 support


0.2.0 (2018-12-26)
------------------

(delayed release, used from @dev branch for 6 months)

* added clickable.bootstrap
* added helpers for sphinx commands
* added workaround for selinux and virtualenv

0.1.1 (2018-02-10)
------------------

* fix rsync ``options`` arg behavior


0.1.0 (2018-02-10)
------------------

* added rsync handler


0.0.3 (2017-10-17)
------------------

* correctly handle clear_env in sphinx:sphinx_script
* update cryptography, tox, sphinx, wheel


0.0.1 (2017-09-10)
------------------

* First release on PyPI.


0.0.2.dev4 (2017-09-10)
-----------------------

* Fixed ignored excludes in lftp_sync
