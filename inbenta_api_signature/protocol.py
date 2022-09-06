# -*- coding: utf-8 -*-
import time
import json
import six
import hmac
from hashlib import sha256


from .url import *

if six.PY3:
    unicode = str

__all__ = ['V1', 'BaseVersion']

class BaseVersion(object):
    pass


class V1(BaseVersion):
    VERSION = 'v1'
    HASH_ALGORITHM = sha256
    SIGNATURE_HEADER = 'x-inbenta-signature'
    SIGNATURE_VERSION_HEADER = 'x-inbenta-signature-version'
    TIMESTAMP_HEADER = 'x-inbenta-timestamp'
    HEADERS = [SIGNATURE_HEADER, TIMESTAMP_HEADER, SIGNATURE_VERSION_HEADER]

    def __init__(self, key, baseUrl=None):
        self._key = key.encode('utf8')
        self._urlPrefix = ""
        if baseUrl:
            self._urlPrefix = list(urlparse(baseUrl))[2]
        self.timestamp = None

    def getHeaders(self, signature):
        return dict(zip(self.HEADERS, [signature, self.timestamp, self.VERSION]))

    def genTimestamp(self):
        return str(int(time.time()))

    def signRequest(self, url, method, params=None, body=None, timestamp=None):
        raw_sig = self._requestBaseString(url, method, params=params, body=body, timestamp=timestamp)
        return self._sign(raw_sig)

    def validateResponse(self, signature, body, timestamp=None):
        '''Verify that the signature and signature match'''
        baseString = self._responseBaseString(body, timestamp)
        expected = self._sign(baseString)
        return signature == expected

    def _requestBaseString(self, url, method, params=None, body=None, timestamp=None):
        '''Builds the base string of the signature hash'''
        self.timestamp = timestamp or self.genTimestamp()
        self.timestamp = self.timestamp if isinstance(self.timestamp, (str, unicode)) else str(self.timestamp)
        urlParts = list(urlparse(url))
        urlPath = self._buildURLPath(urlParts[2])
        qs = parse_queryparams(urlParts[4])
        qs.update(params or {})
        encodedBody = None
        if body is not None:
            body = body if isinstance(body, (str, unicode)) else json.dumps(body)
            encodedBody = quote_plus(body.encode('utf8'))
        elements = [
            method.upper(),
            urlPath,
            self._buildQueryString(qs),
            encodedBody,
            self.timestamp,
            self.VERSION
        ]
        return '&'.join([e for e in elements if e]).encode('utf8')

    def _responseBaseString(self, body, timestamp=None):
        timestamp = timestamp or self.timestamp or self.genTimestamp()
        timestamp = timestamp if isinstance(timestamp, (str, unicode)) else str(timestamp)
        body = json.dumps(body)
        res = [
            self.VERSION,
            timestamp,
            quote_plus(body.encode('utf8'))
        ]
        return "&".join(res).encode('utf8')

    def _buildURLPath(self, url):
        if url.startswith(self._urlPrefix):
            url = url[len(self._urlPrefix):]
        if url and url[0] == '/':
            url = url[1:]
        return quote_plus(url)

    def _buildQueryString(self, queryString):
        '''Returns the encoded query string
        
        Args:
            queryString: a parsed query string in a dictionary form
        '''
        query = {k: unquote_plus(json.dumps(v)) for k, v in queryString.items()}
        query = ["{}={}".format(k, query[k]) for k in sorted(query)]
        return quote("&".join(query), safe='')

    def _sign(self, baseString):
        return hmac.new(self._key, baseString, self.HASH_ALGORITHM).hexdigest()
