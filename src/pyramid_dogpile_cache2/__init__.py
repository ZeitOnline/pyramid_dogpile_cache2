from pyramid_dogpile_cache import build_dogpile_region_settings_from_settings
import beaker.util
import dogpile.cache
import dogpile.cache.exception


CACHE_REGIONS = {}


def get_region(name):
    """This is the main entry point to the caching system; it returns a
    CacheRegion that can be used to cache function results.

    Example usage::

        CACHE = pyramid_dogpile_cache2.get_region('longterm')
        @CACHE.cache_on_arguments()
        def expensive_function(one, two, three):
            # compute stuff
    """
    # Prevent import cycle
    from pyramid_dogpile_cache2.cache import key_generator, sha1_mangle_key

    if name not in CACHE_REGIONS:
        CACHE_REGIONS[name] = dogpile.cache.make_region(
            name,
            function_key_generator=key_generator,
            key_mangler=sha1_mangle_key)
    return CACHE_REGIONS[name]


def clear():
    """Removes all cached values from all configured cache regions."""
    for region in CACHE_REGIONS.values():
        if 'backend' not in region.__dict__:
            continue
        region.backend._cache.clear()


def includeme(config):
    configure_dogpile_cache(config.registry.settings)


def configure_dogpile_cache(settings):
    # This is somewhat inspired by pyramid_dogpile_cache.includeme()
    # and build_dogpile_region_from_dict().
    _parse_dogpile_cache_settings(settings)
    _, region_settings = build_dogpile_region_settings_from_settings(settings)

    for name, settings in region_settings.items():
        # XXX Type conversion for all sorts of settings is woefully incomplete.
        settings['expiration_time'] = int(settings['expiration_time'])
        settings.setdefault(
            'arguments.memcached_expire_time', settings['expiration_time'] +
            int(settings.get(
                'memcache_expire_time_interval', 30)))

        region = get_region(name)
        # XXX kludgy: Remove any existing backend configuration, so
        # configure_dogpile_cache() may be called multiple times (which
        # should only happen in tests).
        region.__dict__.pop('backend', None)
        region.configure_from_config(settings, prefix='')

    # Since get_region() returns an unconfigured region for *any* name you
    # pass in, we make sure that all used regions are configured now.
    for region in CACHE_REGIONS.values():
        if 'backend' not in region.__dict__:
            raise dogpile.cache.exception.RegionNotConfigured(
                'Region %r used in python code, but not configured' %
                region.name)


def _parse_dogpile_cache_settings(settings):
    # XXX Woefully incomplete. This only supports pylibmc, and our specific
    # use-case: all regions use the same memcache settings.
    if 'dogpile_cache.pylibmc_url' in settings:
        settings['dogpile_cache.arguments.url'] = settings[
            'dogpile_cache.pylibmc_url'].split(';')
        del settings['dogpile_cache.pylibmc_url']

    for key in ['dogpile_cache.arguments.lock_timeout',
                'dogpile_cache.arguments.memcache_expire_time']:
        if key in settings:
            settings[key] = int(settings[key])

    behaviors = {}
    behavior_prefix = 'dogpile_cache.pylibmc_behavior.'
    to_remove = []
    for key, value in settings.items():
        if not key.startswith(behavior_prefix):
            continue
        behaviors[key.replace(behavior_prefix, '')] = value
        to_remove.append(key)
    if behaviors:
        convert = beaker.util.coerce_memcached_behaviors
        settings['dogpile_cache.arguments.behaviors'] = convert(behaviors)
        for key in to_remove:
            del settings[key]
