# -*- coding: utf-8 -*-
"""MockUp a server request."""
from io import BytesIO
import json

import urllib3
from requests.adapters import HTTPAdapter
from inbenta_api_signature.protocol import V1

import pytest


class MockServer(HTTPAdapter):
    '''This is only a mock for testing.

    This is not making any requests, only validate the signature'''
    def __init__(self, signatureKey, baseUrl=None, signatureProto=None, *args, **kwargs):
        super(MockServer, self).__init__(*args, **kwargs)
        protoClass = signatureProto or V1
        self._protocol = protoClass(signatureKey, baseUrl=baseUrl)

    def __checkHeaders(self, headers):
        return all([h in headers.keys() for h in self._protocol.HEADERS])

    def send(self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None):
        self.add_headers(request, stream=stream, timeout=timeout, verify=verify, cert=cert, proxies=proxies)
        # Default returns 200 and the same body message
        status = 200
        body = request.body or "No Body"
        # check headers are present
        if self.__checkHeaders(request.headers):
            # Check signature is valid
            timestamp = request.headers[self._protocol.TIMESTAMP_HEADER]
            signature = self._protocol.signRequest(request.url, request.method, params=None, body=request.body, timestamp=timestamp)
            signatureHeaders = self._protocol.getHeaders(signature)
            for name, value in signatureHeaders.items():
                _v = request.headers.get(name)
                if not _v or _v != value:
                    status = 403
                    body = json.dumps({"error" : {"code" : 403, "message": "Headers {} is not correct".format(name)}})
                    break
        else:
            status = 403
            body = json.dumps({"error" : {"code" : 403, "message": "Headers are missing"}})

        headers = urllib3.response.HTTPHeaderDict(request.headers)
        if hasattr(body, 'read'):
            body.seek(0)
        else:
            body = BytesIO(body.encode('utf8'))
        response = urllib3.HTTPResponse(body, headers, status, preload_content=False)
        return self.build_response(request, response)

    def build_response(self, req, resp):
        response = super(MockServer, self).build_response(req, resp)
        if response.status_code // 100 == 2 and self.__checkHeaders(req.headers):
            signature = self._protocol._responseBaseString(response.text)
            signature = self._protocol._sign(signature)
            response.headers.update(self._protocol.getHeaders(signature))
        return response