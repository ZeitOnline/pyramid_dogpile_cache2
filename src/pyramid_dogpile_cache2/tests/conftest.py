import pyramid_dogpile_cache2
import pytest


@pytest.fixture
def empty_config(request):
    request.addfinalizer(pyramid_dogpile_cache2.CACHE_REGIONS.clear)
