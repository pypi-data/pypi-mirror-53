# from hamcrest import *
# from dtest import Dtest
# from pandas import DataFrame
# import json

# connectionConfig = {
#     "host": "localhost:5672",
#     "username": "guest",
#     "password": "guest",
#     "exchange": "logs",
#     "exchange_type": "fanout"
# }
# metadata = {
#     "description": "This is a description of a local test suite",
#     "topic": "test.dtest",
#     "ruleSet": "This is a description of a ruleset",
#     "dataSet": "random_data_set_123912731.csv"
# }

# dt = Dtest(connectionConfig, metadata)

# # A couple examples
# # We use pyhamcrest for the matchers - Documentation: https://github.com/hamcrest/PyHamcrest

# df = DataFrame(data=[0, 1, 20, 34, 1, 23, 1, 5,
#                      6, 88, 2234, 1, 1, 46, 6, 23])

# dt.assert_that("adsasd", is_(instance_of(str)), '', 'Warn')
# dt.assert_that(df, has_length(1), '', 'Fatal')

# print(json.dumps(dt.testSuite.__dict__))
# for result in dt.testSuite.testResultsList:
#     print(json.dumps(result.__dict__))

# dt.publish()
