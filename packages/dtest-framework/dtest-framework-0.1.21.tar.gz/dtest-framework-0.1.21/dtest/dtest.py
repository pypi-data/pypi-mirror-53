from .publishers.rmqhandler import RabbitMQHandler
from .publishers.restkvhandler import RESTKvHandler
from .interfaces.handler import MqHandler, KvHandler
from .vaults.secretsmanager import get_aws_secret
from .schema.results_schema import TestSuiteResultSchema, TestResultSchema

import warnings
from hamcrest.core.matcher import Matcher
from hamcrest.core.string_description import StringDescription
import time
import json


class Dtest():
    def __init__(self, connectionConfig, suiteMetadata, mqHandler=None, kvHandler=None):
        """Initialize the Dtest class

        If you want to use the basic handler(s) built in, define `connectionConfig` as follows:

        ::
            connectionConfig = {
                "queue": { # This will send to RabbitMQ by default unless `mqHandler` is provided
                    "vault": { # Optional - use vault or explicit connection config below
                        "provider": "aws_secrets_manager",
                        "secret_name": "secret_name_here",
                        "region": "us-east-1"
                    },
                    "host": "localhost",
                    "username": "guest",
                    "password": "guest",
                    "exchange": "test.dtest",
                    "exchange_type": "fanout"
                },
                "kv-store": { # This uses two REST calls to get/set key values
                    "api_url": "localhost:8080/api/",
                    "retrieve_path": "getKeyValue/", # Specified 'key' will be appended to the retrieve_path variable
                    "publish_path": "postKeyValue/"
                } 
            }

        :param connectionConfig: A dictionary of the connection configuration
        :param suiteMetadata: A dictionary of the test suite descripiton
        :param mqHandler: An optional message queue handler
        :param kvHandler: An optional key value store handler
        """
        if mqHandler is None and "queue" in connectionConfig:
            if "vault" in connectionConfig["queue"]:
                self._handle_vault(connectionConfig["queue"]["vault"])
            else:
                self.mqHandler = RabbitMQHandler(
                    connectionConfig["queue"]["host"], connectionConfig["queue"]["exchange"], connectionConfig["queue"]["exchange_type"], connectionConfig["queue"]["username"], connectionConfig["queue"]["password"])
        else:
            self.mqHandler = mqHandler

        if kvHandler is None and "kv-store" in connectionConfig:
            self.kvHandler = RESTKvHandler(connectionConfig["kv-store"]["api_url"], connectionConfig["kv-store"]
                                           ["retrieve_path"], connectionConfig["kv-store"]["publish_path"])
        else:
            self.kvHandler = kvHandler

        self.testSuite = TestSuiteResultSchema()
        self.testSuite.startTime = time.time()
        self.testSuite.description = suiteMetadata["description"]
        self.testSuite.topic = suiteMetadata["topic"]
        self.testSuite.ruleSet = suiteMetadata["ruleSet"]
        self.testSuite.dataSet = suiteMetadata["dataSet"]

    def publish(self):
        """Publish the test results to the message queue"""
        if self.mqHandler is None:
            raise Exception(
                'Provide a MqHandler that implements dtest.handler.MqHandler or provide connection configuration via `queue` to `connectionConfig`')
        self.testSuite.testResults = self._convert_list_to_vars(
            self.testSuite.testResultsList)
        self.testSuite.duration = time.time() - self.testSuite.startTime

        finalJSON = json.dumps(self.testSuite.__dict__,
                               default=self._default_json_dumps)

        try:
            self.mqHandler.connect()
            self.mqHandler.publish_results(finalJSON)
            self.mqHandler.close_connection()
            return True
        except:
            print(
                "Error connecting and publishing to RabbitMQ @ " + str(self.mqHandler.host) + ":" + str(self.mqHandler.port) + " on exchange `" + str(self.mqHandler.exchange) + "`")
            raise
        return False

    def publish_key_value(self, key, value):
        """Publish a key/value pair to the key-value store

        :param key: A string representation of the key
        :param value: An Object to store (e.g. array, dict, string)
        """
        if self.kvHandler is None:
            raise Exception(
                'Provide a KvHandler that implements dtest.handler.KvHandler or provide connection configuration via `kv-store` to `connectionConfig`')
        try:
            return self.kvHandler.publish(key, value)
        except:
            print("Error connecting and publishing to Key Value store @ " +
                  self.kvHandler.url + self.kvHandler.pubPath)
            raise
        return False

    def retrieve_key_value(self, key):
        """Retrieve a key/value pair from the key-value store

        :param key: A string representation of the key
        """
        if self.kvHandler is None:
            raise Exception(
                'Provide a KvHandler that implements dtest.handler.KvHandler or provide connection configuration to via `kv-store` to `connectionConfig`')
        try:
            return self.kvHandler.retrieve(key)
        except:
            print("Error connecting and publishing to Key Value store @ " +
                  self.kvHandler.url + self.kvHandler.retrPath)
            raise
        return None

    def _convert_list_to_vars(self, l):
        newList = []
        for i in l:
            newList.append(vars(i))
        return newList

    def _default_json_dumps(self, o):
        if type(o).__name__ == 'int64':
            return int(o)
        raise TypeError

    def add_result(self, obj, reason=None, severity='None'):
        """Add a test result to the suite when a matcher is not needed. (e.g. 
        a statistical score for a field or dataset)

        :param obj: The object to publish 
        :param reason: An optional description of the results being published
        :param severity: An optional severity level - defaults to 0, insignificant
        """
        results = TestResultSchema()
        results.description = reason
        results.severity = severity
        results.startTime = 0
        results.duration = 0
        results.passed = None
        results.actualResult = {}
        results.actualResult["data"] = obj
        self.testSuite.testResultsList.append(results)

    def publish_result(self, obj, reason=None, severity='None'):
        """ Publish a test result when a matcher is not needed. (e.g. 
        a statistical score for a field or dataset)

        :param obj: The object to publish 
        :param reason: An optional description of the results being published
        :param severity: An optional severity level - defaults to 'None', insignificant
        """
        results = TestResultSchema()
        results.description = reason
        results.severity = severity
        results.startTime = 0
        results.duration = 0
        results.passed = None
        results.actualResult = {}
        results.actualResult["data"] = obj
        self.testSuite.testResultsList.append(results)
        self.publish()

    """
    An adaptation of pyhamcrest 'assert_that' by Jon Reid
    __author__ = "Jon Reid"
    __copyright__ = "Copyright 2011 hamcrest.org"
    __license__ = "BSD, see hamcrest-License.txt"
    """

    def assert_that(self, arg1, arg2=None, arg3='', arg4='None'):
        """Asserts that actual value satisfies matcher. (Can also assert plain
        boolean condition.)

        :param actual: The object to evaluate as the actual value.
        :param matcher: The matcher to satisfy as the expected condition.
        :param reason: Optional explanation to include in failure description.

        ``assert_that`` passes the actual value to the matcher for evaluation. If
        the matcher is not satisfied, an exception is thrown describing the
        mismatch.

        ``assert_that`` is designed to integrate well with PyUnit and other unit
        testing frameworks. The exception raised for an unmet assertion is an
        :py:exc:`AssertionError`, which PyUnit reports as a test failure.

        With a different set of parameters, ``assert_that`` can also verify a
        boolean condition:

        .. function:: assert_that(assertion[, reason])

        :param assertion:  Boolean condition to verify.
        :param reason:  Optional explanation to include in failure description.
        :param severity: Optional severity level if test fails.

        This is equivalent to the :py:meth:`~unittest.TestCase.assertTrue` method
        of :py:class:`unittest.TestCase`, but offers greater flexibility in test
        writing by being a standalone function.

        """
        if isinstance(arg2, Matcher):
            return self._assert_match(actual=arg1, matcher=arg2, reason=arg3, severity=arg4)
        else:
            if isinstance(arg1, Matcher):
                warnings.warn(
                    "arg1 should be boolean, but was {}".format(type(arg1)))
            self._assert_bool(assertion=arg1, reason=arg2)

    def _assert_match(self, actual, matcher, reason, severity):
        results = TestResultSchema()
        results.description = reason
        results.startTime = time.time()
        results.severity = severity

        if not matcher.matches(actual):
            results.duration = time.time() - results.startTime
            results.passed = False

            description = StringDescription()
            description.append_text('Expected: ')     \
                .append_description_of(matcher)
            results.expectedResult = description.out

            description = StringDescription()
            description.append_text('but: ')
            matcher.describe_mismatch(actual, description)
            results.actualResult = {}
            results.actualResult["description"] = description.out

            if isinstance(actual, list):
                results.actualResult["data"] = actual[:10]
            elif type(actual).__name__ == 'DataFrame':
                results.actualResult["data"] = actual.head(
                    10).to_dict(orient='records')

            self.testSuite.testResultsList.append(results)
            return False
        else:
            results.duration = time.time() - results.startTime
            results.passed = True

            description = StringDescription()
            description.append_text('Expected: ')     \
                .append_description_of(matcher)
            results.expectedResult = description.out
            self.testSuite.testResultsList.append(results)

            return True

    def _assert_bool(self, assertion, reason=None):
        if not assertion:
            if not reason:
                reason = 'Assertion failed'
            raise AssertionError(reason)

    def _handle_vault(self, config):
        if config["provider"] == "aws_secrets_manager":
            config = get_aws_secret(config["secret_name"], config["region"])
            self.mqHandler = RabbitMQHandler(
                config["host"], config["exchange"], config["exchange_type"], config["username"], config["password"])
        else:
            raise Exception(
                'Could not find a valid vault provider')
