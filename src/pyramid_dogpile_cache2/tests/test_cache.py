# coding: utf-8
import dogpile.cache.util
import pyramid_dogpile_cache2.cache
import pytest


def test_key_generator_handles_non_ascii_arguments():
    gen = dogpile.cache.util.function_key_generator(None, lambda: None)
    with pytest.raises(UnicodeEncodeError):
        gen(u'föö')

    gen = pyramid_dogpile_cache2.cache.key_generator(None, lambda: None)
    gen(u'föö')


def test_mangle_key_handles_non_ascii_arguments():
    with pytest.raises(UnicodeEncodeError):
        dogpile.cache.util.sha1_mangle_key(u'föö')

    pyramid_dogpile_cache2.cache.sha1_mangle_key(u'föö')


def test_key_generator_adds_class_name_for_methods():
    def plain_function():
        pass

    class Foo(object):

        def method(self):
            pass

    gen = dogpile.cache.util.function_key_generator(None, plain_function)
    assert gen() == 'pyramid_dogpile_cache2.tests.test_cache:plain_function|'
    gen = dogpile.cache.util.function_key_generator(None, Foo().method)
    assert gen() == 'pyramid_dogpile_cache2.tests.test_cache:method|'

    gen = pyramid_dogpile_cache2.cache.key_generator(None, plain_function)
    assert gen() == 'pyramid_dogpile_cache2.tests.test_cache.plain_function|'
    gen = pyramid_dogpile_cache2.cache.key_generator(None, Foo().method)
    assert gen() == 'pyramid_dogpile_cache2.tests.test_cache.Foo.method|'
