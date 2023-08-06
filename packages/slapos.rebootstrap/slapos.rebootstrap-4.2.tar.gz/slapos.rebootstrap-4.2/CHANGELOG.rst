Changes
=======

4.2 (2019-10-10)
----------------

- Support python provided by a part that does not need install.
  This fixes installation of slapos software release which python comes
  already installed in shared parts from an outer slapos.

4.1 (2017-06-06)
----------------

- Fix MANIFEST.in: some files were missing.

4.0 (2017-06-05)
----------------

Complete reimplementation:

- Work entirely in-place, even to switch to a different version of Python.
- Update bin/buildout to immediately use the wanted Python on subsequent
  buildout runs.

For SlapOS, the second point is required to have the instanciation done
with the built Python.

3.10 (2017-03-15)
-----------------

* Drop zc.buildout version pinning to prevent loop in case of version
  change.

3.9 (2017-03-15)
----------------

* Drop zc.buildout version pinning in reboot() to prevent loop in
  case of version change.

3.8 (2017-03-13)
----------------

* Use a dedicated rebootstrap directory only if
  buildout:rebootstrap-directory is set.

3.7 (2016-08-18)
----------------

* Preserve bin-directory for generate bin/buildout on the
  appropriate location.

3.6 (2016-06-30)
----------------

* Add more parameters for the use case with slapos.package.

3.5 (2016-06-10)
----------------

* Explicitly specify the python interpreter and the config file when
  invoking a new buildout process to build rebootstrap directory.

3.4 (2016-06-10)
----------------

* Use a dedicated buildout directory for building a rebootstrap
  python. The change in 3.2 was wrong because it causes infinite loop
  of rebootstrap and build for different version of python.

3.3 (2016-01-20)
----------------

* Ignore MissingSection exception in _uninstall_part().

3.2 (2015-11-10)
----------------

* Support zc.buildout >= 2.0.0.
* Same parts directory as the normal buildout is used so that we can
  build faster and also make the code simpler.
* Python part is now specified by `python` parameter in `buildout`
  section.
* Restart automatically with the original python when running python
  part is removed.

3.1 (2011-06-24)
----------------

* Support eggs parameter in rebootstrap section in order to add additional
  eggs for rebootstrapped buildout.

3.0 (2011-05-27)
----------------

* Renamed from slapos.tool.rebootstrap 2.4
