from dogpile.cache.backends.memory import MemoryBackend
from pyramid_dogpile_cache2 import configure_dogpile_cache, get_region
import dogpile.cache.backends.memcached
import dogpile.cache.exception
import pytest


def test_sets_backend_for_regions(empty_config):
    configure_dogpile_cache({
        'dogpile_cache.regions': 'foo, bar',
        'dogpile_cache.backend': 'dogpile.cache.memory',
        'dogpile_cache.expiration_time': '1',
    })
    assert isinstance(get_region('foo').backend, MemoryBackend)
    assert isinstance(get_region('bar').backend, MemoryBackend)


def test_converts_expiration_time(empty_config):
    configure_dogpile_cache({
        'dogpile_cache.regions': 'foo',
        'dogpile_cache.backend': 'dogpile.cache.memory',
        'dogpile_cache.expiration_time': '1',
    })
    assert get_region('foo').expiration_time == 1


def test_converts_expiration_time_to_int(empty_config):
    configure_dogpile_cache({
        'dogpile_cache.regions': 'foo',
        'dogpile_cache.backend': 'dogpile.cache.memory',
        'dogpile_cache.expiration_time': '1',
    })
    assert get_region('foo').expiration_time == 1


def test_sets_memcache_expire_time_to_later_than_expiration_time(
        empty_config, monkeypatch):
    monkeypatch.setattr(
        dogpile.cache.backends.memcached.PylibmcBackend, '_imports',
        lambda self: None)
    configure_dogpile_cache({
        'dogpile_cache.regions': 'foo',
        'dogpile_cache.backend': 'dogpile.cache.pylibmc',
        'dogpile_cache.pylibmc_url': 'http://localhost:8899',
        'dogpile_cache.expiration_time': '1',
        'dogpile_cache.memcache_expire_time_interval': '5'
    })
    assert get_region('foo').backend.memcached_expire_time == 6


def test_sets_pylibmc_behaviours(empty_config, monkeypatch):
    monkeypatch.setattr(
        dogpile.cache.backends.memcached.PylibmcBackend, '_imports',
        lambda self: None)
    configure_dogpile_cache({
        'dogpile_cache.regions': 'foo',
        'dogpile_cache.backend': 'dogpile.cache.pylibmc',
        'dogpile_cache.pylibmc_url': 'http://localhost:8899',
        'dogpile_cache.expiration_time': '1',
        'dogpile_cache.pylibmc_behavior.send_timeout': '5',
    })
    assert get_region('foo').backend.behaviors == {'send_timeout': 5}


def test_unconfigured_region_raises(empty_config):
    get_region('bar')
    with pytest.raises(dogpile.cache.exception.RegionNotConfigured):
        configure_dogpile_cache({
            'dogpile_cache.regions': 'foo',
            'dogpile_cache.backend': 'dogpile.cache.memory',
            'dogpile_cache.expiration_time': '1',
        })
