======================
pyramid_dogpile_cache2
======================

.. image:: https://travis-ci.org/ZeitOnline/pyramid_dogpile_cache2.png
   :target: https://travis-ci.org/ZeitOnline/pyramid_dogpile_cache2

Small `dogpile.cache`_ configuration and access package. It is inspired by
`pyramid_dogpile_cache`_, which we found unusable since it insists on
configuring the cache regions in its ``get_region()`` API -- but if you want to
use the ``@cache_on_arguments`` decorator, that is at **import time**, where no
configuration exists yet. Our package wants to perform the configuration during
the WSGI application setup instead.

This package is compatible with Python version 2.7 and 3.4.

.. _`dogpile.cache`: https://pypi.python.org/pypi/dogpile.cache
.. _`pyramid_dogpile_cache`: https://pypi.python.org/pypi/pyramid_dogpile_cache


Usage
=====

The package offers only one API function; it returns a dogpile.cache
``CacheRegion``::

    from pyramid_dogpile_cache import get_region
    region = get_region('foo')

As said above, this is safe to call at import time, so you can go on like this::

    @region.cache_on_arguments()
    def expensive_function(one, two, three):
        # compute stuff


Setup / Pyramid
===============

Include the package, either in code::

    config = Configurator(...)
    config.include('pyramid_dogpile_cache2')

or in the ini file::

    pyramid.includes = pyramid_dogpile_cache2


Setup / Paste
=============

For non-Pyramid WSGI applications that use a paste.ini file, you need to call::

    def my_paste_app_factory(global_conf, **local_conf):
        pyramid_dogpile_cache2.configure_dogpile_cache(local_conf)
        return my_wsgi_callable


Settings
========

The settings support of pyramid_dogpile_cache unfortunately is quite incomplete
(e.g. it does not even convert ``expiration_time`` to ``int``). The support of
this packages is a little better, but still very much incomplete: we support
the in-memory and memcached backends (pylibmc to be precise), and only the same
backend and configuration for all cache regions.

The following settings are supported:

``dogpile_cache.regions``

    A list of region names that should be configured (separated by either
    spaces or commas).

``dogpile_cache.backend``

    The default backend for cache regions (e.g. ``'dogpile.cache.memory'``,
    ``dogpile.cache.pylibmc``, etc.).

``dogpile_cache.REGION.backend``

   Backend for the given region.

``dogpile_cache.expiration_time``

    The default expiration time. Can be overridden for individual regions (in
    seconds).

``dogpile_cache.REGION.expiration_time``

    The expiration time for the given cache region (in seconds).

``dogpile_cache.arguments.*``

    Defaults for backend arguments. Can be overridden for individual regions.

``dogpile_cache.REGION.arguments.*``

    Backend arguments for the given cache region.

Backend arguments work only for strings, thus we support some custom treatment:

``dogpile_cache.pylibmc_url``

    A list of memcached servers, separated by ``;``.

``dogpile_cache.pylibmc_behavior.*``

    Set `pylibmc behaviours`_, see `coerce_memached_behaviors`_ for which
    subkeys are supported.


.. _`pylibmc behaviours`: http://sendapatch.se/projects/pylibmc/behaviors.html
.. _`coerce_memached_behaviors`: https://github.com/bbangert/beaker/blob/master/beaker/util.py#L343

Note: As opposed to pyramid_dogpile_cache we don't support overriding the
key_generator or key_mangler functions yet; we preconfigure them with enhanced
versions of dogpile.cache that support non-ascii function arguments and
generating cache keys for methods that include the class name.
