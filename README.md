# Introduction
This client helps you signing requests following Inbenta's API Signature Protocol, which is an extra security step that some Inbenta APIs include.

The protocol details are explained in Inbenta's developers site (https://developers.inbenta.io/general/authorization/signing-api-requests), but in summary what it does is adding some additional header to API requests.

In detail, any request that is signed using Inbenta's Signature Protocol must provide the following headers:
* `x-inbenta-key`: Like other Inbenta API, this API requires authorization.
* `authorization`: Like other Inbenta API, this API requires authorization.
* `x-inbenta-signature`: This is the header containing the signature this client will help you build.
* `x-inbenta-signature-version`: This header identifies the protocol to follow when signing requests (defaults to `"v1"`).
* `x-inbenta-timestamp`: This header carries a unix timestamp of the time of the request. This is a security measure to prevent replay attacks (defaults to `time()`).


# Installation
You should load this library using [pip](https://pypi.org/project/pip/).

## Locally using pipenv
If you don't have full access to install dependencies in your environment, you can install this library using [pipenv](https://github.com/pypa/pipenv).
```bash
$ pipenv --python 2.7  # you can also use --python 3.6
$ pipenv install -e git+git@github.com:inbenta-products/api-signature-client-python.git#egg=inbenta_signature_client
$ pipenv shell
$ python my-testing-script.py  # or just type `python` to run any code within the python shell
```

## Globally
Just run the following command:
```bash
$ pip install -e git+git@github.com:inbenta-products/api-signature-client-python.git#egg=inbenta_signature_client
```

# Usage
The SignatureClient can be used in 2 different ways, which are detailed in the following sections. You will find two examples:

* `Using an HTTPAdapter`: there is a `SignatureAdapter` which will help you create requests that are always signed as soon as you plug in the adapter. This is a mechanism thought to simplify the process.
* `Using string values`: if you don't have sessions or you just don't want to use adapters in your application, this option works with the values needed for each step instead of wrapping them within an adapter.

## Before running the examples

See that some constants are defined in the following examples, which are:
* `INBENTA_AUTH_URL`: The Auth URL against you authenticate for all Inbenta API's (usually `https://api.inbenta.io/v1/auth`).

Then, from Backstage > Administration > Reporting API section you will be able to obtain the rest of constants:
* `INBENTA_API_KEY`: The reporting key to authenticate against Auth.
* `INBENTA_API_SECRET`: The reporting secret to authenticate against Auth.
* `INBENTA_REPORTING_API_URL`: The endpoint to target to obtain your reporting data.
* `INBENTA_API_SIGNATURE_KEY`: The token to correctly sign your requests.


## Examples

### Using an HTTPAdapter

```python
import requests
import json
from inbenta_api_signature import SignatureAdapter

INBENTA_AUTH_URL = ""
INBENTA_REPORTING_API_URL = ""
INBENTA_API_KEY = ""
INBENTA_API_SECRET = ""
INBENTA_API_SIGNATURE_KEY = ""

# 1. Inbenta Auth
headers = {
    "x-inbenta-key": INBENTA_API_KEY
}
body = {
    "secret": INBENTA_API_SECRET
}
auth = requests.post(INBENTA_AUTH_URL, headers=headers, json=body)
headers['Authorization'] = "Bearer {}".format(auth.json()['accessToken'])

# 2. Create session for signed requests
s = requests.session()
s.mount(INBENTA_REPORTING_API_URL, SignatureAdapter(INBENTA_API_SIGNATURE_KEY, INBENTA_REPORTING_API_URL))

url = "{}/{}".format(INBENTA_REPORTING_API_URL, "v1/events/user_questions")

# 3. Send request to API
response = s.get(url=url, headers=headers)
if response.status_code != 200:
    print ("Request failed...")
print(json.dumps(response.json(), indent=4, sort_keys=True))

# 4. Validate response signature
validSignature = response.validSignature
if validSignature is None:
    print ("The response could not be validated possibly to an error")
elif validSignature:
    print ("The signature in response is valid")
else:
    print ("The signature in response is not valid")

```

### Using string values

```python
import requests
import json
from inbenta_api_signature import SignatureClient

INBENTA_AUTH_URL = ""
INBENTA_REPORTING_API_URL = ""
INBENTA_API_KEY = ""
INBENTA_API_SECRET = ""
INBENTA_API_SIGNATURE_KEY = ""

# 1. Inbenta Auth
headers = {
    "x-inbenta-key": INBENTA_API_KEY
}
body = {
    "secret": INBENTA_API_SECRET
}
auth = requests.post(INBENTA_AUTH_URL, headers=headers, json=body)
headers['Authorization'] = "Bearer {}".format(auth.json()['accessToken'])

# 2. Create Request
client = SignatureClient(INBENTA_API_SIGNATURE_KEY, INBENTA_REPORTING_API_URL)
url = "{}/{}".format(INBENTA_REPORTING_API_URL, "v1/events/user_questions")

# 3. Sign request
signatureHeaders = client.signRequest(url, body=None, method="GET")
headers.update(signatureHeaders)

# 4. Send request to API
response = requests.get(url=url, headers=headers)
if response.status_code != 200:
    print ("Request failed...")
print(json.dumps(response.json(), indent=4, sort_keys=True))

# 5. Validate response signature
validSignature = client.validateResponse(response.headers.get(client.SIGNATURE_HEADER), response.text)
if validSignature is None:
    print ("The response could not be validated possibly to an error")
elif validSignature:
    print ("The signature in response is valid")
else:
    print ("The signature in response is not valid")

```

# Running the tests
To run the test suite you can use [tox](https://pypi.org/project/tox/):
```
$ pip install --user tox  # to install tox, if you don't have it already
$ tox
```

# Dependencies
The Requests Library is optional but recomended to be able to use the Adapter
