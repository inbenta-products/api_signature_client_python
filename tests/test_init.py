# -*- coding: utf-8 -*-
import os
from copy import deepcopy
import json
import requests
import pytest

from inbenta_api_signature import SignatureClient
from inbenta_api_signature import changeBaseHTTPAdapter
from inbenta_api_signature import V1
from mockServer import MockServer


def mockRequest(signatureKey, baseUrl=None):
    # This will mock the request to use the MockServer class
    s = requests.Session()
    s.mount('http://', MockServer(signatureKey, baseUrl=baseUrl))
    s.mount('https://', MockServer(signatureKey, baseUrl=baseUrl))
    return s


TEST_INPUT = [
    pytest.param(
        {
            "signatureKey": 'my-signature-key',
            "baseUrl": 'https://foo.bar/v1',
            "timestamp": 1552647740,
            "request": {
                "method": "GET",
                "url": 'v1/foo/bar/bG9nOjozOTUyMjEyNzg4MTk3NTk0NTU=',
                "body": '',
                "params": ''
            }
        },
        {
            "status_code": 200,
            "validSignature": True
        },
        id= "url-no-query"
    ),
    pytest.param(
        {
            "signatureKey": 'my-signature-key',
            "baseUrl": 'https://foo.bar',
            "timestamp": 1552647740,
            "request": {
                "method": "GET",
                "url": 'v1/foo/',
                "params": {
                    "date_from": "2019-01-01",
                    "date_to": "2019-01-3"
                }
            }
        },
        {
            "status_code": 200,
            "validSignature": True
        },
        id= "url-with-params"
    ),
]



@pytest.mark.parametrize("test_input,expected", TEST_INPUT)
def test_signatureclient(test_input, expected):
    INBENTA_API_SIGNATURE_KEY = test_input['signatureKey']
    BASE_URL = test_input.get('baseUrl')
    mRequest = mockRequest(INBENTA_API_SIGNATURE_KEY, baseUrl=BASE_URL)
    client = SignatureClient(INBENTA_API_SIGNATURE_KEY, baseUrl=BASE_URL)

    test_request = test_input['request']
    method = test_request['method']
    url = os.path.join(BASE_URL, test_request['url'])
    signatureHeaders = client.signRequest(url, params=test_request['params'], body=test_request.get('body'), method=method, timestamp=test_input.get('timestamp'))
    
    headers = {}
    headers.update(signatureHeaders)

    body = test_request.get('body')
    if isinstance(body, dict):
        body = json.dumps(body)
    response = getattr(mRequest, method.lower())(url, params=test_request['params'], data=body, headers=headers)

    assert response.status_code == expected['status_code']
    validSignature = client.validateResponse(response.headers.get(client.SIGNATURE_HEADER), response.text)
    assert validSignature == expected['validSignature']



@pytest.mark.parametrize("test_input,expected", TEST_INPUT)
def test_httpadapter(test_input, expected):
    INBENTA_API_SIGNATURE_KEY = test_input['signatureKey']
    BASE_URL = test_input.get('baseUrl')
    AdapterWithMockServer = changeBaseHTTPAdapter(MockServer)

    mRequest = requests.Session()
    mRequest.mount('http://', AdapterWithMockServer(INBENTA_API_SIGNATURE_KEY, BASE_URL, None, INBENTA_API_SIGNATURE_KEY, BASE_URL))
    mRequest.mount('https://', AdapterWithMockServer(INBENTA_API_SIGNATURE_KEY, BASE_URL, None, INBENTA_API_SIGNATURE_KEY, BASE_URL))
    # mockRequest(INBENTA_API_SIGNATURE_KEY, baseUrl=BASE_URL)

    test_request = test_input['request']
    method = test_request['method']
    url = os.path.join(BASE_URL, test_request['url'])
    headers = {}
    body = test_request.get('body')
    if isinstance(body, dict):
        body = json.dumps(body)
    response = getattr(mRequest, method.lower())(url, params=test_request['params'], data=body, headers=headers)

    # print("response: {}".format(response.text))
    assert response.status_code == expected['status_code']
    assert response.validSignature == expected['validSignature']


def test_signatureclient_class():
    assert SignatureClient('examplekey', signatureVersion=V1('examplekey'))
    assert SignatureClient('examplekey', signatureVersion='v1')
    with pytest.raises(ValueError):
        SignatureClient('examplekey', signatureVersion=V1)
    with pytest.raises(ValueError):
        SignatureClient('examplekey', signatureVersion="v2")


def test_changebasehttpadapter():
    class T1(requests.adapters.HTTPAdapter):
        pass
    t = T1()
    class T2(object):
        pass

    assert changeBaseHTTPAdapter(T1)
    with pytest.raises(TypeError):
        changeBaseHTTPAdapter(t)
    with pytest.raises(TypeError):
        changeBaseHTTPAdapter(T2)
