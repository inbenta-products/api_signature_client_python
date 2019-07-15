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
