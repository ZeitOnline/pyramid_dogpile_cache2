# coding: utf-8
from pyramid_dogpile_cache2 import get_region
import dogpile.cache.util
import pyramid_dogpile_cache2.cache


def test_key_generator_handles_type_annotations():
    def function_with_annotations() -> None:
        pass

    gen = pyramid_dogpile_cache2.cache.key_generator(None, function_with_annotations)
    assert gen() == 'pyramid_dogpile_cache2.tests.test_cache.function_with_annotations|'


def test_mangle_key_handles_non_ascii_arguments():
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
    foo = Foo()
    gen = pyramid_dogpile_cache2.cache.key_generator(None, foo.method)
    assert gen(foo) == 'pyramid_dogpile_cache2.tests.test_cache.Foo.method|'


def test_methods_are_detected_when_decorated(empty_config):
    region = get_region('test')
    region.configure('dogpile.cache.memory')

    class Foo(object):

        @region.cache_on_arguments()
        def method(self):
            return 42

    Foo().method()
    assert region.get('pyramid_dogpile_cache2.tests.test_cache.Foo.method|') == 42
