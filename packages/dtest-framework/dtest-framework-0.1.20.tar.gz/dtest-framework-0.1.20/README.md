# dtest

[![CircleCI](https://circleci.com/gh/sjensen85/dtest/tree/master.svg?style=svg)](https://circleci.com/gh/sjensen85/dtest/tree/master)
[![Requirements Status](https://requires.io/github/sjensen85/dtest/requirements.svg?branch=master)](https://requires.io/github/sjensen85/dtest/requirements/?branch=master)

A library to facilitate the testing of data inside data pipelines. Results are pushed to a messaging queue of some sort for consumption by applications, persistence, etc.

Supported messaging queues / streaming platforms

- [x] RabbitMQ
- [ ] MQTT
- [ ] Redis
- [ ] Kafka
- [ ] Kinesis

Supported secrets managers

- [x] AWS Secrets Manager
- [ ] Hashicorp Vault

## Installation

`pip3 install dtest-framework`

## Unit Tests

Testing is set up using Pytest

Install Pytest with `pip3 install -U pytest`

Run the tests with `pytest` in the root directory.

## Quick Start

```
from dtest.dtest import Dtest
from hamcrest import *


# If publishing to a RabbitMQ queue, specify 'queue' \
# If publishing to a key-value store, specify 'kv-store' \
# Or specify both

connectionConfig = {
    "queue": {
        "host": "localhost",
        "username": "guest",
        "password": "guest",
        "exchange": "test.dtest",
        "exchange_type": "fanout"
    },
    "kv-store": {
        "api_url": "localhost:8080/api/",
        "retrieve_path": "getKeyValue/",
        "publish_path": "postKeyValue/"
    }
}
metadata = {
    "description": "This is a test of the assertCondition",
    "topic": "test.dtest",
    "ruleSet": "Testing some random data",
    "dataSet": "random_data_set_123912731.csv"
}

dt = Dtest(connectionConfig, metadata)

dsQubert = [0,1]

dt.assert_that(dsQubert, has_length(2))
// True

dt.publish()
// Publishes test suite to MQ server


////////////////////////////////////////
// Store value in KV store for later use
dt.publishKeyValue('some-descriptor-dsQubert-length', len(dqQubert))

// Retrieve value from KV store to compare other files against
avg_count = dt.retrieveKeyValue('some-descriptor-dsQubert-length')

dt.assert_that(dsQubert, has_length(avg_count))
```

## Connection configuration

There are two options for providing the connection configuration for the publisher - the default way described above and by storing your configuration in a secrets manager. To utilize a secrets manager, use a connectionConfig similar to:

```
connectionConfig = {
    "queue": {
        "vault": {
                    "provider": "aws_secrets_manager",
                    "secret_name": "secret_name_here",
                    "region": "us-east-1"
                }
    }
}
```

Here we are giving the provider name `aws_secrets_manager`, the key to use to retrieve the secret `secret_name`, and the region in which Secrets Manager is hosted. `secret_name` and `region` are passed to `boto3` directly. `region_name` is provided when initializing the `boto3` session and `secret_name` is provided to the `boto3.secretsmanager.get_secret_value()` function as `SecretId`.

## Custom handlers

It is possible to create custom message queue and key value store handlers. Implement a class that inherits from `dtest.handler.MqHandler` or `dtest.handler.KvHandler` depending on your needs.

```

class MqHandler:

    @classmethod
    def version(self): return "1.0"

    @abstractmethod
    def connect(self): raise NotImplementedError

    @abstractmethod
    def publishResults(self): raise NotImplementedError

    @abstractmethod
    def closeConnection(self): raise NotImplementedError


class KvHandler:

    @classmethod
    def version(self): return "1.0"

    @abstractmethod
    def retrieve(self): raise NotImplementedError

    @abstractmethod
    def publish(self): raise NotImplementedError

```

## Package dependencies

I did not want to require that all dependencies of every module need to be installed. As such, the following packages need to be installed via `pip` if you would like to utilize the specified functionality

| Package | Dependent module/functionality |
| ------- | ------------------------------ |
| boto3   | `vaults.secretsmanager`        |
|         |                                |
| pandas  | Local testing with `pytest`    |

#### CI/CD

- Use the standard `ecs` labeled Jenkins agent
- Performs tests on master commits and PRs
- Does not deploy to PyPI automatically
