import pytest

import pyramid_dogpile_cache2


@pytest.fixture
def empty_config(request):
    request.addfinalizer(pyramid_dogpile_cache2.CACHE_REGIONS.clear)
