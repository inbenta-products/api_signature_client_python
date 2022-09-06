# -*- coding: utf-8 -*-
import pytest

from inbenta_api_signature import url

@pytest.mark.parametrize("test_input,expected", [
    ('https://example.test/foo/bar', {}),
    ('https://example.test/foo?a=10', {'a': '10'}),
    ('https://example.test/foo?a=10&b=Hello%20world', {'a': '10', 'b': "Hello world"}),
    ('foo/bar?q=1&q=2&q=3', {'q': '3'}),
    ('foo/bar?q[]=1&q[]=2', {'q': ['1','2']}),
    ('foo/bar?q[]=1,2&q[]=3,4', {'q': ['1,2', '3,4']}),
    ('foo/?uq=%22pregunta%20en%20catal%5Cu00e0%22', {'uq': '"pregunta en catal\\u00e0"'}),
    ('foo/?a=pregunta+en+catal%C3%A0', {'a': 'pregunta en català'}),
    ('foo/?tz=Europe/Madrid', {'tz': 'Europe/Madrid'}),
    ('foo/?tz=Europe%2FMadrid', {'tz': 'Europe/Madrid'}),
])
def test_queryparams(test_input, expected):
    # Should match with php parse_str() function
    obj = url.urlparse(test_input)
    assert url.parse_queryparams(obj.query) == expected
