import unittest
import json
from crawling_gocd.inputs_parser import InputsParser

class InputsParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = InputsParser("tests/unit/resources/inputs.yaml")

    def test_should_generate_inputs_object_correctly(self):
        result = self.parser.parse()
        self.assertEqual("".join(str(x) for x in result),
                         "{ name: accounting-plus-master, calcConfig: { groupedStages: {'ci': ['code-scan', 'test-integration', 'build'], 'qa': ['flyway-qa', 'deploy-qa']}, startTime: 2019-07-01 00:00:00, endTime: 2019-08-12 23:59:59 } }")
