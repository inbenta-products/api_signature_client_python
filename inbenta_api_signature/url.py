# -*- coding: utf-8 -*-
"""URL Parse functions."""

try:
    # Python 3
    from urllib.parse import urlparse, unquote_plus, quote, parse_qs, quote_plus
except ImportError:
    # Python 2
    from urllib import quote, unquote_plus, quote_plus
    from urlparse import urlparse, parse_qs


__all__ = ['urlparse', 'parse_queryparams', 'quote', 'unquote_plus', 'quote_plus']


def parse_queryparams(qs, **kwargs):
    """parse_qs that Mimic the PHP parse_str() query Params parser."""
    params = {}
    for key, val in parse_qs(qs, **kwargs).items():
        if key.endswith('[]'):
            key = key[:-2]
        elif isinstance(val, list):
            val = val[-1]
        params[key] = val
    return params
