# -*- coding: utf-8 -*-
"""Test the Protocol specification."""

from collections import OrderedDict
from copy import deepcopy

from inbenta_api_signature.protocol import V1

import pytest
from freezegun import freeze_time


@pytest.mark.parametrize("test_input,expected", [

    (
        {}, ""
    ),
    (
        {"a": 10, "b": 20, "c": "Foo Bar"},
        "a%3D10%26b%3D20%26c%3D%22Foo%20Bar%22"
    ),
    (

        {"c": "Foo Bar", "b": 20, "a": 10},
        "a%3D10%26b%3D20%26c%3D%22Foo%20Bar%22",
    ),
    (
        OrderedDict({"a": 10, "b": 20, "c": "Foo Bar"}),
        "a%3D10%26b%3D20%26c%3D%22Foo%20Bar%22"
    ),
    (

        OrderedDict({"c": "Foo Bar", "b": 20, "a": 10}),
        "a%3D10%26b%3D20%26c%3D%22Foo%20Bar%22",
    )
])
def test_protocol_v1_querystring(test_input, expected):
    proto = V1('examplekey')
    assert proto._buildQueryString(test_input) == expected



@freeze_time('2019-04-18 10:00:00')
@pytest.mark.parametrize("test_input,expected", [
    pytest.param(
        {
            "signatureKey": 'my-signature-key',
            "timestamp": 1552647740,
            "request": {
                "method": "GET",
                "url": 'v1/foo/bar/bG9nOjozOTUyMjEyNzg4MTk3NTk0NTU=',
                "body": '',
            },
            "response": {
                "body": '{"total_count":1,"offset":0,"length":1000,"results":[{"event_id":"bG9nOjozOTUyMjEyNzg4MTk3NTk0NTU=","date":"2018-12-03T10:32:00+00:00","user_question":"flight","log_type":"SEARCH","has_matching":true,"matchings":[{"id_content":25,"external":false},{"id_content":4,"external":false},{"id_content":32,"external":false},{"id_content":1,"external":false},{"id_content":37,"external":false}],"user_type":0,"env":"production"}]}',
            }
        },
        {
            "request_baseString": 'GET&v1%2Ffoo%2Fbar%2FbG9nOjozOTUyMjEyNzg4MTk3NTk0NTU%3D&1552647740&v1',
            "response_baseString": 'v1&1552647740&%22%7B%5C%22total_count%5C%22%3A1%2C%5C%22offset%5C%22%3A0%2C%5C%22length%5C%22%3A1000%2C%5C%22results%5C%22%3A%5B%7B%5C%22event_id%5C%22%3A%5C%22bG9nOjozOTUyMjEyNzg4MTk3NTk0NTU%3D%5C%22%2C%5C%22date%5C%22%3A%5C%222018-12-03T10%3A32%3A00%2B00%3A00%5C%22%2C%5C%22user_question%5C%22%3A%5C%22flight%5C%22%2C%5C%22log_type%5C%22%3A%5C%22SEARCH%5C%22%2C%5C%22has_matching%5C%22%3Atrue%2C%5C%22matchings%5C%22%3A%5B%7B%5C%22id_content%5C%22%3A25%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A4%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A32%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A1%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A37%2C%5C%22external%5C%22%3Afalse%7D%5D%2C%5C%22user_type%5C%22%3A0%2C%5C%22env%5C%22%3A%5C%22production%5C%22%7D%5D%7D%22'
        },
        id= "url-no-query"
    ),
    pytest.param(
        {
            "signatureKey": 'my-signature-key',
            "timestamp": 1552647740,
            "request": {
                "method": "GET",
                'url': 'v1/foo/bar?date_from=2019-01-01&date_to=2019-01-31&env=development,production',
                'body': ''
            },
            "response": {
                "body": '{"total_count":5,"offset":0,"length":1000,"results":[{"event_id":"bG9nOjozOTYwNjA5NTE4MzQ1MTA4ODM=","date":"2019-01-10T09:38:13+00:00","user_question":"How can I book a flight?","log_type":"SEARCH","has_matching":true,"matchings":[{"id_content":25,"external":false},{"id_content":30,"external":false},{"id_content":1,"external":false},{"id_content":13,"external":false},{"id_content":16,"external":false}],"user_type":0,"env":"production"},{"event_id":"bG9nOjozOTYwNjA5NTAyNjMwMDY5OTI=","date":"2019-01-10T09:38:06+00:00","user_question":"flight","log_type":"SEARCH","has_matching":true,"matchings":[{"id_content":25,"external":false},{"id_content":4,"external":false},{"id_content":32,"external":false},{"id_content":1,"external":false},{"id_content":37,"external":false}],"user_type":0,"env":"production"},{"event_id":"bG9nOjozOTYwNDUyNjA2NTAyOTc0MDY=","date":"2019-01-09T16:36:39+00:00","user_question":"flight","log_type":"SEARCH","has_matching":true,"matchings":[{"id_content":25,"external":false},{"id_content":4,"external":false},{"id_content":32,"external":false},{"id_content":1,"external":false},{"id_content":37,"external":false}],"user_type":0,"env":"development"},{"event_id":"bG9nOjozOTYwNDQ4NTQ5MzM4NDQ3MDg=","date":"2019-01-09T16:10:14+00:00","user_question":"flight","log_type":"SEARCH","has_matching":true,"matchings":[{"id_content":25,"external":false},{"id_content":4,"external":false},{"id_content":32,"external":false},{"id_content":1,"external":false},{"id_content":37,"external":false}],"user_type":0,"env":"development"},{"event_id":"bG9nOjozOTYwNDQzNjU5NjIwMzA0OTU=","date":"2019-01-09T15:38:24+00:00","user_question":"flight change","log_type":"SEARCH","has_matching":true,"matchings":[{"id_content":10,"external":false}],"user_type":0,"env":"development"}]}',
            }
        },
        {
            "request_baseString": 'GET&v1%2Ffoo%2Fbar&date_from%3D%222019-01-01%22%26date_to%3D%222019-01-31%22%26env%3D%22development%2Cproduction%22&1552647740&v1',
            "response_baseString": 'v1&1552647740&%22%7B%5C%22total_count%5C%22%3A5%2C%5C%22offset%5C%22%3A0%2C%5C%22length%5C%22%3A1000%2C%5C%22results%5C%22%3A%5B%7B%5C%22event_id%5C%22%3A%5C%22bG9nOjozOTYwNjA5NTE4MzQ1MTA4ODM%3D%5C%22%2C%5C%22date%5C%22%3A%5C%222019-01-10T09%3A38%3A13%2B00%3A00%5C%22%2C%5C%22user_question%5C%22%3A%5C%22How+can+I+book+a+flight%3F%5C%22%2C%5C%22log_type%5C%22%3A%5C%22SEARCH%5C%22%2C%5C%22has_matching%5C%22%3Atrue%2C%5C%22matchings%5C%22%3A%5B%7B%5C%22id_content%5C%22%3A25%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A30%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A1%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A13%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A16%2C%5C%22external%5C%22%3Afalse%7D%5D%2C%5C%22user_type%5C%22%3A0%2C%5C%22env%5C%22%3A%5C%22production%5C%22%7D%2C%7B%5C%22event_id%5C%22%3A%5C%22bG9nOjozOTYwNjA5NTAyNjMwMDY5OTI%3D%5C%22%2C%5C%22date%5C%22%3A%5C%222019-01-10T09%3A38%3A06%2B00%3A00%5C%22%2C%5C%22user_question%5C%22%3A%5C%22flight%5C%22%2C%5C%22log_type%5C%22%3A%5C%22SEARCH%5C%22%2C%5C%22has_matching%5C%22%3Atrue%2C%5C%22matchings%5C%22%3A%5B%7B%5C%22id_content%5C%22%3A25%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A4%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A32%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A1%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A37%2C%5C%22external%5C%22%3Afalse%7D%5D%2C%5C%22user_type%5C%22%3A0%2C%5C%22env%5C%22%3A%5C%22production%5C%22%7D%2C%7B%5C%22event_id%5C%22%3A%5C%22bG9nOjozOTYwNDUyNjA2NTAyOTc0MDY%3D%5C%22%2C%5C%22date%5C%22%3A%5C%222019-01-09T16%3A36%3A39%2B00%3A00%5C%22%2C%5C%22user_question%5C%22%3A%5C%22flight%5C%22%2C%5C%22log_type%5C%22%3A%5C%22SEARCH%5C%22%2C%5C%22has_matching%5C%22%3Atrue%2C%5C%22matchings%5C%22%3A%5B%7B%5C%22id_content%5C%22%3A25%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A4%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A32%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A1%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A37%2C%5C%22external%5C%22%3Afalse%7D%5D%2C%5C%22user_type%5C%22%3A0%2C%5C%22env%5C%22%3A%5C%22development%5C%22%7D%2C%7B%5C%22event_id%5C%22%3A%5C%22bG9nOjozOTYwNDQ4NTQ5MzM4NDQ3MDg%3D%5C%22%2C%5C%22date%5C%22%3A%5C%222019-01-09T16%3A10%3A14%2B00%3A00%5C%22%2C%5C%22user_question%5C%22%3A%5C%22flight%5C%22%2C%5C%22log_type%5C%22%3A%5C%22SEARCH%5C%22%2C%5C%22has_matching%5C%22%3Atrue%2C%5C%22matchings%5C%22%3A%5B%7B%5C%22id_content%5C%22%3A25%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A4%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A32%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A1%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A37%2C%5C%22external%5C%22%3Afalse%7D%5D%2C%5C%22user_type%5C%22%3A0%2C%5C%22env%5C%22%3A%5C%22development%5C%22%7D%2C%7B%5C%22event_id%5C%22%3A%5C%22bG9nOjozOTYwNDQzNjU5NjIwMzA0OTU%3D%5C%22%2C%5C%22date%5C%22%3A%5C%222019-01-09T15%3A38%3A24%2B00%3A00%5C%22%2C%5C%22user_question%5C%22%3A%5C%22flight+change%5C%22%2C%5C%22log_type%5C%22%3A%5C%22SEARCH%5C%22%2C%5C%22has_matching%5C%22%3Atrue%2C%5C%22matchings%5C%22%3A%5B%7B%5C%22id_content%5C%22%3A10%2C%5C%22external%5C%22%3Afalse%7D%5D%2C%5C%22user_type%5C%22%3A0%2C%5C%22env%5C%22%3A%5C%22development%5C%22%7D%5D%7D%22'
        },
        id="url-with-query"
    ),
    pytest.param(
        {
            "signatureKey": 'my-signature-key',
            "timestamp": 1552647740,
            "request": {
                "method": "GET",
                'url': 'v1/foo/bar?date_from=2019-01-01&date_to=2019-01-31&env=production&user_question=flight',
                'body': ''
            },
            "response": {
                "body": '{"total_count":2,"offset":0,"length":1000,"results":[{"event_id":"bG9nOjozOTYwNjA5NTE4MzQ1MTA4ODM=","date":"2019-01-10T09:38:13+00:00","user_question":"How can I book a flight?","log_type":"SEARCH","has_matching":true,"matchings":[{"id_content":25,"external":false},{"id_content":30,"external":false},{"id_content":1,"external":false},{"id_content":13,"external":false},{"id_content":16,"external":false}],"user_type":0,"env":"production"},{"event_id":"bG9nOjozOTYwNjA5NTAyNjMwMDY5OTI=","date":"2019-01-10T09:38:06+00:00","user_question":"flight","log_type":"SEARCH","has_matching":true,"matchings":[{"id_content":25,"external":false},{"id_content":4,"external":false},{"id_content":32,"external":false},{"id_content":1,"external":false},{"id_content":37,"external":false}],"user_type":0,"env":"production"}]}',
            }
        },
        {
            "request_baseString": 'GET&v1%2Ffoo%2Fbar&date_from%3D%222019-01-01%22%26date_to%3D%222019-01-31%22%26env%3D%22production%22%26user_question%3D%22flight%22&1552647740&v1',
            "response_baseString": 'v1&1552647740&%22%7B%5C%22total_count%5C%22%3A2%2C%5C%22offset%5C%22%3A0%2C%5C%22length%5C%22%3A1000%2C%5C%22results%5C%22%3A%5B%7B%5C%22event_id%5C%22%3A%5C%22bG9nOjozOTYwNjA5NTE4MzQ1MTA4ODM%3D%5C%22%2C%5C%22date%5C%22%3A%5C%222019-01-10T09%3A38%3A13%2B00%3A00%5C%22%2C%5C%22user_question%5C%22%3A%5C%22How+can+I+book+a+flight%3F%5C%22%2C%5C%22log_type%5C%22%3A%5C%22SEARCH%5C%22%2C%5C%22has_matching%5C%22%3Atrue%2C%5C%22matchings%5C%22%3A%5B%7B%5C%22id_content%5C%22%3A25%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A30%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A1%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A13%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A16%2C%5C%22external%5C%22%3Afalse%7D%5D%2C%5C%22user_type%5C%22%3A0%2C%5C%22env%5C%22%3A%5C%22production%5C%22%7D%2C%7B%5C%22event_id%5C%22%3A%5C%22bG9nOjozOTYwNjA5NTAyNjMwMDY5OTI%3D%5C%22%2C%5C%22date%5C%22%3A%5C%222019-01-10T09%3A38%3A06%2B00%3A00%5C%22%2C%5C%22user_question%5C%22%3A%5C%22flight%5C%22%2C%5C%22log_type%5C%22%3A%5C%22SEARCH%5C%22%2C%5C%22has_matching%5C%22%3Atrue%2C%5C%22matchings%5C%22%3A%5B%7B%5C%22id_content%5C%22%3A25%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A4%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A32%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A1%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A37%2C%5C%22external%5C%22%3Afalse%7D%5D%2C%5C%22user_type%5C%22%3A0%2C%5C%22env%5C%22%3A%5C%22production%5C%22%7D%5D%7D%22'
        },
        id="url-with-more-complex-query"
    ),
    pytest.param(
        {
            "signatureKey": 'my-signature-key',
            "timestamp": 1552647740,
            "request": {
                "method": "GET",
                'url': 'v1/foo/bar?date_from=2019-01-01&date_to=2019-01-31&env=production&user_question=flight offer',
                'body': ''
            },
            "response": {
                "body": '{"total_count":2,"offset":0,"length":1000,"results":[{"event_id":"bG9nOjozOTYwNjA5NTE4MzQ1MTA4ODM=","date":"2019-01-10T09:38:13+00:00","user_question":"How can I book a flight?","log_type":"SEARCH","has_matching":true,"matchings":[{"id_content":25,"external":false},{"id_content":30,"external":false},{"id_content":1,"external":false},{"id_content":13,"external":false},{"id_content":16,"external":false}],"user_type":0,"env":"production"},{"event_id":"bG9nOjozOTYwNjA5NTAyNjMwMDY5OTI=","date":"2019-01-10T09:38:06+00:00","user_question":"flight","log_type":"SEARCH","has_matching":true,"matchings":[{"id_content":25,"external":false},{"id_content":4,"external":false},{"id_content":32,"external":false},{"id_content":1,"external":false},{"id_content":37,"external":false}],"user_type":0,"env":"production"}]}',
            }
        },
        {
            "request_baseString": 'GET&v1%2Ffoo%2Fbar&date_from%3D%222019-01-01%22%26date_to%3D%222019-01-31%22%26env%3D%22production%22%26user_question%3D%22flight%20offer%22&1552647740&v1',
            "response_baseString": 'v1&1552647740&%22%7B%5C%22total_count%5C%22%3A2%2C%5C%22offset%5C%22%3A0%2C%5C%22length%5C%22%3A1000%2C%5C%22results%5C%22%3A%5B%7B%5C%22event_id%5C%22%3A%5C%22bG9nOjozOTYwNjA5NTE4MzQ1MTA4ODM%3D%5C%22%2C%5C%22date%5C%22%3A%5C%222019-01-10T09%3A38%3A13%2B00%3A00%5C%22%2C%5C%22user_question%5C%22%3A%5C%22How+can+I+book+a+flight%3F%5C%22%2C%5C%22log_type%5C%22%3A%5C%22SEARCH%5C%22%2C%5C%22has_matching%5C%22%3Atrue%2C%5C%22matchings%5C%22%3A%5B%7B%5C%22id_content%5C%22%3A25%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A30%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A1%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A13%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A16%2C%5C%22external%5C%22%3Afalse%7D%5D%2C%5C%22user_type%5C%22%3A0%2C%5C%22env%5C%22%3A%5C%22production%5C%22%7D%2C%7B%5C%22event_id%5C%22%3A%5C%22bG9nOjozOTYwNjA5NTAyNjMwMDY5OTI%3D%5C%22%2C%5C%22date%5C%22%3A%5C%222019-01-10T09%3A38%3A06%2B00%3A00%5C%22%2C%5C%22user_question%5C%22%3A%5C%22flight%5C%22%2C%5C%22log_type%5C%22%3A%5C%22SEARCH%5C%22%2C%5C%22has_matching%5C%22%3Atrue%2C%5C%22matchings%5C%22%3A%5B%7B%5C%22id_content%5C%22%3A25%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A4%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A32%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A1%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A37%2C%5C%22external%5C%22%3Afalse%7D%5D%2C%5C%22user_type%5C%22%3A0%2C%5C%22env%5C%22%3A%5C%22production%5C%22%7D%5D%7D%22'
        },
        id="url-with-query-with-spaces"
    ),  
    pytest.param(
        {
            "signatureKey": 'my-signature-key',
            "timestamp": 1552647740,
            "request": {
                "method": "GET",
                'url': 'v1/foo/bar?date_from=2019-01-01&date_to=2019-01-31&env=production&user_question=flight+offer',
                'body': ''
            },
            "response": {
                "body":'{"total_count":2,"offset":0,"length":1000,"results":[{"event_id":"bG9nOjozOTYwNjA5NTE4MzQ1MTA4ODM=","date":"2019-01-10T09:38:13+00:00","user_question":"How can I book a flight?","log_type":"SEARCH","has_matching":true,"matchings":[{"id_content":25,"external":false},{"id_content":30,"external":false},{"id_content":1,"external":false},{"id_content":13,"external":false},{"id_content":16,"external":false}],"user_type":0,"env":"production"},{"event_id":"bG9nOjozOTYwNjA5NTAyNjMwMDY5OTI=","date":"2019-01-10T09:38:06+00:00","user_question":"flight","log_type":"SEARCH","has_matching":true,"matchings":[{"id_content":25,"external":false},{"id_content":4,"external":false},{"id_content":32,"external":false},{"id_content":1,"external":false},{"id_content":37,"external":false}],"user_type":0,"env":"production"}]}',
            }
        },
        {
            "request_baseString": 'GET&v1%2Ffoo%2Fbar&date_from%3D%222019-01-01%22%26date_to%3D%222019-01-31%22%26env%3D%22production%22%26user_question%3D%22flight%20offer%22&1552647740&v1',
            "response_baseString": 'v1&1552647740&%22%7B%5C%22total_count%5C%22%3A2%2C%5C%22offset%5C%22%3A0%2C%5C%22length%5C%22%3A1000%2C%5C%22results%5C%22%3A%5B%7B%5C%22event_id%5C%22%3A%5C%22bG9nOjozOTYwNjA5NTE4MzQ1MTA4ODM%3D%5C%22%2C%5C%22date%5C%22%3A%5C%222019-01-10T09%3A38%3A13%2B00%3A00%5C%22%2C%5C%22user_question%5C%22%3A%5C%22How+can+I+book+a+flight%3F%5C%22%2C%5C%22log_type%5C%22%3A%5C%22SEARCH%5C%22%2C%5C%22has_matching%5C%22%3Atrue%2C%5C%22matchings%5C%22%3A%5B%7B%5C%22id_content%5C%22%3A25%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A30%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A1%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A13%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A16%2C%5C%22external%5C%22%3Afalse%7D%5D%2C%5C%22user_type%5C%22%3A0%2C%5C%22env%5C%22%3A%5C%22production%5C%22%7D%2C%7B%5C%22event_id%5C%22%3A%5C%22bG9nOjozOTYwNjA5NTAyNjMwMDY5OTI%3D%5C%22%2C%5C%22date%5C%22%3A%5C%222019-01-10T09%3A38%3A06%2B00%3A00%5C%22%2C%5C%22user_question%5C%22%3A%5C%22flight%5C%22%2C%5C%22log_type%5C%22%3A%5C%22SEARCH%5C%22%2C%5C%22has_matching%5C%22%3Atrue%2C%5C%22matchings%5C%22%3A%5B%7B%5C%22id_content%5C%22%3A25%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A4%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A32%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A1%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A37%2C%5C%22external%5C%22%3Afalse%7D%5D%2C%5C%22user_type%5C%22%3A0%2C%5C%22env%5C%22%3A%5C%22production%5C%22%7D%5D%7D%22'
        },
        id="url-with-query-with-spaces-as-plus-sign"
    ), 
    pytest.param(
        {
            "signatureKey": 'my-signature-key',
            "timestamp": 1552647740,
            "request": {
                "method": "GET",
                'url': 'v1/foo/bar?date_from=2019-01-01&date_to=2019-01-31&env=production&user_question=flight%20offer',
                'body': ''
            },
            "response": {
                "body": '{"total_count":2,"offset":0,"length":1000,"results":[{"event_id":"bG9nOjozOTYwNjA5NTE4MzQ1MTA4ODM=","date":"2019-01-10T09:38:13+00:00","user_question":"How can I book a flight?","log_type":"SEARCH","has_matching":true,"matchings":[{"id_content":25,"external":false},{"id_content":30,"external":false},{"id_content":1,"external":false},{"id_content":13,"external":false},{"id_content":16,"external":false}],"user_type":0,"env":"production"},{"event_id":"bG9nOjozOTYwNjA5NTAyNjMwMDY5OTI=","date":"2019-01-10T09:38:06+00:00","user_question":"flight","log_type":"SEARCH","has_matching":true,"matchings":[{"id_content":25,"external":false},{"id_content":4,"external":false},{"id_content":32,"external":false},{"id_content":1,"external":false},{"id_content":37,"external":false}],"user_type":0,"env":"production"}]}'
            }
        },
        {
            "request_baseString": 'GET&v1%2Ffoo%2Fbar&date_from%3D%222019-01-01%22%26date_to%3D%222019-01-31%22%26env%3D%22production%22%26user_question%3D%22flight%20offer%22&1552647740&v1',
            "response_baseString": 'v1&1552647740&%22%7B%5C%22total_count%5C%22%3A2%2C%5C%22offset%5C%22%3A0%2C%5C%22length%5C%22%3A1000%2C%5C%22results%5C%22%3A%5B%7B%5C%22event_id%5C%22%3A%5C%22bG9nOjozOTYwNjA5NTE4MzQ1MTA4ODM%3D%5C%22%2C%5C%22date%5C%22%3A%5C%222019-01-10T09%3A38%3A13%2B00%3A00%5C%22%2C%5C%22user_question%5C%22%3A%5C%22How+can+I+book+a+flight%3F%5C%22%2C%5C%22log_type%5C%22%3A%5C%22SEARCH%5C%22%2C%5C%22has_matching%5C%22%3Atrue%2C%5C%22matchings%5C%22%3A%5B%7B%5C%22id_content%5C%22%3A25%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A30%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A1%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A13%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A16%2C%5C%22external%5C%22%3Afalse%7D%5D%2C%5C%22user_type%5C%22%3A0%2C%5C%22env%5C%22%3A%5C%22production%5C%22%7D%2C%7B%5C%22event_id%5C%22%3A%5C%22bG9nOjozOTYwNjA5NTAyNjMwMDY5OTI%3D%5C%22%2C%5C%22date%5C%22%3A%5C%222019-01-10T09%3A38%3A06%2B00%3A00%5C%22%2C%5C%22user_question%5C%22%3A%5C%22flight%5C%22%2C%5C%22log_type%5C%22%3A%5C%22SEARCH%5C%22%2C%5C%22has_matching%5C%22%3Atrue%2C%5C%22matchings%5C%22%3A%5B%7B%5C%22id_content%5C%22%3A25%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A4%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A32%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A1%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A37%2C%5C%22external%5C%22%3Afalse%7D%5D%2C%5C%22user_type%5C%22%3A0%2C%5C%22env%5C%22%3A%5C%22production%5C%22%7D%5D%7D%22'
        },
        id="url-with-query-with-spaces-as-%20"
    ),
    pytest.param(
        {
            "signatureKey": 'my-signature-key',
            "timestamp": 1552647740,
            "request": {
                "method": "GET",
                'url': 'v1/foo/bar?date_from=2019-01-01&date_to=2019-01-31&env=production&user_question=pregunta en català',
                'body': ''
            },
            "response": {
                "body": '{"total_count":2,"offset":0,"length":1000,"results":[{"event_id":"bG9nOjozOTYwNjA5NTE4MzQ1MTA4ODM=","date":"2019-01-10T09:38:13+00:00","user_question":"How can I book a flight?","log_type":"SEARCH","has_matching":true,"matchings":[{"id_content":25,"external":false},{"id_content":30,"external":false},{"id_content":1,"external":false},{"id_content":13,"external":false},{"id_content":16,"external":false}],"user_type":0,"env":"production"},{"event_id":"bG9nOjozOTYwNjA5NTAyNjMwMDY5OTI=","date":"2019-01-10T09:38:06+00:00","user_question":"flight","log_type":"SEARCH","has_matching":true,"matchings":[{"id_content":25,"external":false},{"id_content":4,"external":false},{"id_content":32,"external":false},{"id_content":1,"external":false},{"id_content":37,"external":false}],"user_type":0,"env":"production"}]}',
            }
        },
        {
            "request_baseString": 'GET&v1%2Ffoo%2Fbar&date_from%3D%222019-01-01%22%26date_to%3D%222019-01-31%22%26env%3D%22production%22%26user_question%3D%22pregunta%20en%20catal%5Cu00e0%22&1552647740&v1',
            "response_baseString": 'v1&1552647740&%22%7B%5C%22total_count%5C%22%3A2%2C%5C%22offset%5C%22%3A0%2C%5C%22length%5C%22%3A1000%2C%5C%22results%5C%22%3A%5B%7B%5C%22event_id%5C%22%3A%5C%22bG9nOjozOTYwNjA5NTE4MzQ1MTA4ODM%3D%5C%22%2C%5C%22date%5C%22%3A%5C%222019-01-10T09%3A38%3A13%2B00%3A00%5C%22%2C%5C%22user_question%5C%22%3A%5C%22How+can+I+book+a+flight%3F%5C%22%2C%5C%22log_type%5C%22%3A%5C%22SEARCH%5C%22%2C%5C%22has_matching%5C%22%3Atrue%2C%5C%22matchings%5C%22%3A%5B%7B%5C%22id_content%5C%22%3A25%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A30%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A1%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A13%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A16%2C%5C%22external%5C%22%3Afalse%7D%5D%2C%5C%22user_type%5C%22%3A0%2C%5C%22env%5C%22%3A%5C%22production%5C%22%7D%2C%7B%5C%22event_id%5C%22%3A%5C%22bG9nOjozOTYwNjA5NTAyNjMwMDY5OTI%3D%5C%22%2C%5C%22date%5C%22%3A%5C%222019-01-10T09%3A38%3A06%2B00%3A00%5C%22%2C%5C%22user_question%5C%22%3A%5C%22flight%5C%22%2C%5C%22log_type%5C%22%3A%5C%22SEARCH%5C%22%2C%5C%22has_matching%5C%22%3Atrue%2C%5C%22matchings%5C%22%3A%5B%7B%5C%22id_content%5C%22%3A25%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A4%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A32%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A1%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A37%2C%5C%22external%5C%22%3Afalse%7D%5D%2C%5C%22user_type%5C%22%3A0%2C%5C%22env%5C%22%3A%5C%22production%5C%22%7D%5D%7D%22',
        },
        id="url-with-query-with-special-chars"
    ),  
    pytest.param(
        {
            "signatureKey": 'my-signature-key',
            "timestamp": 1552647740,
            "request": {
                "method": "GET",
                'url': 'v1/foo/bar?date_from=2019-01-01&date_to=2019-01-31&env=production&user_question=pregunta%20en%20catal%C3%A0',
                'body': ''
            },
            "response": {
                "body":'{"total_count":2,"offset":0,"length":1000,"results":[{"event_id":"bG9nOjozOTYwNjA5NTE4MzQ1MTA4ODM=","date":"2019-01-10T09:38:13+00:00","user_question":"How can I book a flight?","log_type":"SEARCH","has_matching":true,"matchings":[{"id_content":25,"external":false},{"id_content":30,"external":false},{"id_content":1,"external":false},{"id_content":13,"external":false},{"id_content":16,"external":false}],"user_type":0,"env":"production"},{"event_id":"bG9nOjozOTYwNjA5NTAyNjMwMDY5OTI=","date":"2019-01-10T09:38:06+00:00","user_question":"flight","log_type":"SEARCH","has_matching":true,"matchings":[{"id_content":25,"external":false},{"id_content":4,"external":false},{"id_content":32,"external":false},{"id_content":1,"external":false},{"id_content":37,"external":false}],"user_type":0,"env":"production"}]}',
            }
        },
        {
            "request_baseString": 'GET&v1%2Ffoo%2Fbar&date_from%3D%222019-01-01%22%26date_to%3D%222019-01-31%22%26env%3D%22production%22%26user_question%3D%22pregunta%20en%20catal%5Cu00e0%22&1552647740&v1',
            "response_baseString": 'v1&1552647740&%22%7B%5C%22total_count%5C%22%3A2%2C%5C%22offset%5C%22%3A0%2C%5C%22length%5C%22%3A1000%2C%5C%22results%5C%22%3A%5B%7B%5C%22event_id%5C%22%3A%5C%22bG9nOjozOTYwNjA5NTE4MzQ1MTA4ODM%3D%5C%22%2C%5C%22date%5C%22%3A%5C%222019-01-10T09%3A38%3A13%2B00%3A00%5C%22%2C%5C%22user_question%5C%22%3A%5C%22How+can+I+book+a+flight%3F%5C%22%2C%5C%22log_type%5C%22%3A%5C%22SEARCH%5C%22%2C%5C%22has_matching%5C%22%3Atrue%2C%5C%22matchings%5C%22%3A%5B%7B%5C%22id_content%5C%22%3A25%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A30%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A1%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A13%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A16%2C%5C%22external%5C%22%3Afalse%7D%5D%2C%5C%22user_type%5C%22%3A0%2C%5C%22env%5C%22%3A%5C%22production%5C%22%7D%2C%7B%5C%22event_id%5C%22%3A%5C%22bG9nOjozOTYwNjA5NTAyNjMwMDY5OTI%3D%5C%22%2C%5C%22date%5C%22%3A%5C%222019-01-10T09%3A38%3A06%2B00%3A00%5C%22%2C%5C%22user_question%5C%22%3A%5C%22flight%5C%22%2C%5C%22log_type%5C%22%3A%5C%22SEARCH%5C%22%2C%5C%22has_matching%5C%22%3Atrue%2C%5C%22matchings%5C%22%3A%5B%7B%5C%22id_content%5C%22%3A25%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A4%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A32%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A1%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A37%2C%5C%22external%5C%22%3Afalse%7D%5D%2C%5C%22user_type%5C%22%3A0%2C%5C%22env%5C%22%3A%5C%22production%5C%22%7D%5D%7D%22'
        },
        id="url-with-query-with-special-chars-already-encoded"
    ),
    pytest.param(
        {
            "signatureKey": 'my-signature-key',
            "timestamp": 1552647740,
            "request": {
                "method": "GET",
                'url': 'v1/foo/bar?date_from=2019-01-01&date_to=2019-01-31&env=production&timezone=Asia/Tokyo',
                'body': ''
            },
            "response": {
                "body": '{"total_count":2,"offset":0,"length":1000,"results":[{"event_id":"bG9nOjozOTYwNjA5NTE4MzQ1MTA4ODM=","date":"2019-01-10T09:38:13+00:00","user_question":"How can I book a flight?","log_type":"SEARCH","has_matching":true,"matchings":[{"id_content":25,"external":false},{"id_content":30,"external":false},{"id_content":1,"external":false},{"id_content":13,"external":false},{"id_content":16,"external":false}],"user_type":0,"env":"production"},{"event_id":"bG9nOjozOTYwNjA5NTAyNjMwMDY5OTI=","date":"2019-01-10T09:38:06+00:00","user_question":"flight","log_type":"SEARCH","has_matching":true,"matchings":[{"id_content":25,"external":false},{"id_content":4,"external":false},{"id_content":32,"external":false},{"id_content":1,"external":false},{"id_content":37,"external":false}],"user_type":0,"env":"production"}]}',
            }
        },
        {
            "request_baseString": 'GET&v1%2Ffoo%2Fbar&date_from%3D%222019-01-01%22%26date_to%3D%222019-01-31%22%26env%3D%22production%22%26timezone%3D%22Asia%2FTokyo%22&1552647740&v1',
            "response_baseString": 'v1&1552647740&%22%7B%5C%22total_count%5C%22%3A2%2C%5C%22offset%5C%22%3A0%2C%5C%22length%5C%22%3A1000%2C%5C%22results%5C%22%3A%5B%7B%5C%22event_id%5C%22%3A%5C%22bG9nOjozOTYwNjA5NTE4MzQ1MTA4ODM%3D%5C%22%2C%5C%22date%5C%22%3A%5C%222019-01-10T09%3A38%3A13%2B00%3A00%5C%22%2C%5C%22user_question%5C%22%3A%5C%22How+can+I+book+a+flight%3F%5C%22%2C%5C%22log_type%5C%22%3A%5C%22SEARCH%5C%22%2C%5C%22has_matching%5C%22%3Atrue%2C%5C%22matchings%5C%22%3A%5B%7B%5C%22id_content%5C%22%3A25%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A30%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A1%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A13%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A16%2C%5C%22external%5C%22%3Afalse%7D%5D%2C%5C%22user_type%5C%22%3A0%2C%5C%22env%5C%22%3A%5C%22production%5C%22%7D%2C%7B%5C%22event_id%5C%22%3A%5C%22bG9nOjozOTYwNjA5NTAyNjMwMDY5OTI%3D%5C%22%2C%5C%22date%5C%22%3A%5C%222019-01-10T09%3A38%3A06%2B00%3A00%5C%22%2C%5C%22user_question%5C%22%3A%5C%22flight%5C%22%2C%5C%22log_type%5C%22%3A%5C%22SEARCH%5C%22%2C%5C%22has_matching%5C%22%3Atrue%2C%5C%22matchings%5C%22%3A%5B%7B%5C%22id_content%5C%22%3A25%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A4%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A32%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A1%2C%5C%22external%5C%22%3Afalse%7D%2C%7B%5C%22id_content%5C%22%3A37%2C%5C%22external%5C%22%3Afalse%7D%5D%2C%5C%22user_type%5C%22%3A0%2C%5C%22env%5C%22%3A%5C%22production%5C%22%7D%5D%7D%22',
        },
        id="url-with-query-with-slash"
    ),
    pytest.param(
        {
            "signatureKey": 'my-signature-key',
            "timestamp": 1552647740,
            "request": {
                "method": "GET",
                'url': 'v1/foo/bar',
                'body': 'date_from=2019-01-01&date_to=2019-01-31&env=production&user_question=flight',
            },
            "response": {
                "body":'{"error":{"message":"Signature provided is not valid","code":403}}',
            }
        },
        {
            "request_baseString": 'GET&v1%2Ffoo%2Fbar&date_from%3D2019-01-01%26date_to%3D2019-01-31%26env%3Dproduction%26user_question%3Dflight&1552647740&v1',
            "response_baseString": 'v1&1552647740&%22%7B%5C%22error%5C%22%3A%7B%5C%22message%5C%22%3A%5C%22Signature+provided+is+not+valid%5C%22%2C%5C%22code%5C%22%3A403%7D%7D%22'
        },
        id="url-with-body"
    ),
    pytest.param(
        {
            "signatureKey": 'my-signature-key',
            "request": {
                "method": "GET",
                'url': 'v1/foo/bar',
                'body': 'date_from=2019-01-01&date_to=2019-01-31&env=production&user_question=flight',
            },
            "response": {
                "body":'{"error":{"message":"Signature provided is not valid","code":403}}',
            }
        },
        {
            "request_baseString": 'GET&v1%2Ffoo%2Fbar&date_from%3D2019-01-01%26date_to%3D2019-01-31%26env%3Dproduction%26user_question%3Dflight&1555581600&v1',
            "response_baseString": 'v1&1555581600&%22%7B%5C%22error%5C%22%3A%7B%5C%22message%5C%22%3A%5C%22Signature+provided+is+not+valid%5C%22%2C%5C%22code%5C%22%3A403%7D%7D%22'
        },
        id="no-timestamp-set"
    ),
])
def test_protocol_v1(test_input, expected):
    proto = V1(key=test_input['signatureKey'])
    # Check Request
    request = deepcopy(test_input['request'])
    if test_input.get('timestamp'):
        request['timestamp'] = test_input['timestamp']
    signed = proto.signRequest(**request)
    assert signed == proto._sign(expected['request_baseString'].encode('utf-8'))
    # Check Response
    response = {
        'signature': proto._sign(expected['response_baseString'].encode('utf-8')),
        'body': test_input['response']['body'],
    }
    if test_input.get('timestamp'):
        response['timestamp'] = test_input['timestamp']
    assert proto.validateResponse(**response)
