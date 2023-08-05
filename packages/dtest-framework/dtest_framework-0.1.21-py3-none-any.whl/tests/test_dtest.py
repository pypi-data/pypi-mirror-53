from pytest_mock import mocker
import json

from hamcrest import *
from dtest import Dtest
from pandas import DataFrame
from dtest.publishers.rmqhandler import RabbitMQHandler
from dtest.publishers.restkvhandler import RESTKvHandler
from dtest.schema.results_schema import TestResultSchema, TestSuiteResultSchema

connectionConfig = {
    "queue": {
        "host": "localhost",
        "username": "guest",
        "password": "guest",
        "exchange": "logs",
        "exchange_type": "fanout"
    },
    "kv-store": {
        "api_url": "localhost:3000/api/",
        "retrieve_path": "getKeyValue/",
        "publish_path": "postKeyValue/"
    }
}
metadata = {
    "description": "This is a test suite",
    "topic": "test.dtest",
    "ruleSet": "Testing some random things",
    "dataSet": "random_data_set_123912731.csv"
}


def test_dtest_rmq(mocker):
    mqHandler = mocker.Mock()

    dt = Dtest(connectionConfig, metadata, mqHandler=mqHandler)

    df = DataFrame(data=[0, 1, 20, 34, 1, 23, 1, 5,
                         6, 88, 2234, 1, 1, 46, 6, 23])

    assert dt.assert_that(df, has_length(1)) == False

    assert dt.assert_that([0, 1], has_length(2), '', 'Warn') == True

    assert dt.assert_that([0, 1], has_length(1), '', 'Fatal') == False

    for result in dt.testSuite.testResultsList:
        assert isinstance(result, TestResultSchema)

    assert dt.publish() == True

    assert isinstance(dt.testSuite, TestSuiteResultSchema)

    finalJSON = json.dumps(dt.testSuite.__dict__,
                           default=dt._default_json_dumps)

    mqHandler.connect.assert_called_once_with()
    mqHandler.publish_results.assert_called_once_with(finalJSON)


def test_dtest_kv(mocker):
    kvHandler = mocker.Mock()
    kvHandler.retrieve.return_value = True
    kvHandler.publish.return_value = {"ok": 1}

    dt = Dtest(connectionConfig, metadata, kvHandler=kvHandler)

    assert dt.publish_key_value('test', 'value') == {"ok": 1}
    assert dt.retrieve_key_value('test') == True

    kvHandler.publish.assert_called_with('test', 'value')
    kvHandler.retrieve.assert_called_with('test')
