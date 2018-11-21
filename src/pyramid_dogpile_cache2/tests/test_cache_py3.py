import dogpile.cache.util
import pyramid_dogpile_cache2.cache
import pytest


@pytest.mark.skipif(
    dogpile.util.compat.py2k,
    reason='Python 2 does not support type annotation syntax')
def test_key_generator_handles_type_annotations():
    def function_with_annotations() -> None:
        pass

    gen = pyramid_dogpile_cache2.cache.key_generator(None, function_with_annotations)
    assert gen() == 'pyramid_dogpile_cache2.tests.test_cache_py3.function_with_annotations|'
