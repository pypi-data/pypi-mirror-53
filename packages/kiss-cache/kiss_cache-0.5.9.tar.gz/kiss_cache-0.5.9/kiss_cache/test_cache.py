from typing import Set, List
from unittest.mock import Mock
from hypothesis import given
from hypothesis.strategies import sets, integers, lists, dictionaries, characters, randoms
from kiss_cache import Cache


class TestCache:

    @given(sets(integers(), min_size=1, max_size=1000))
    def test_cache_keys_length(self, x: Set[int]):
        cache = Cache()

        @cache.memoize()
        def cached_func(val):
            return val

        for i in x:
            cached_func(i)

        assert len(cache.store.store.keys()) == len(x)

    @given(lists(integers(), min_size=1, max_size=1000))
    def test_body_execution(self, x: List[int]):
        cache = Cache()

        mock = Mock()

        @cache.memoize()
        def cached_func(val):
            mock()
            return val

        for i in x:
            cached_func(i)

        assert mock.call_count == len(set(x))

    @given(dictionaries(characters(), randoms()))
    def test_cache_key_generation(self, x: dict):
        cache = Cache()

        print(x)

        @cache.memoize()
        def cached_func(*args, **kwargs):
            return args, kwargs

        cached_func(**x)

        print(set(x.keys()))

        assert len(cache.store.store.keys()) == len(set(x.keys()) or 1)
