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

    def test_should_return_customize_type_class(self):
        self.parser.inputs.update(
            {"output_class_name": "crawling_gocd.outputs.Output"})
        clazz = self.parser.outputCustomizeClazz()
        self.assertEqual(str(clazz), "<class 'crawling_gocd.outputs.Output'>")

    def test_should_return_default_type_class(self):
        clazz = self.parser.outputCustomizeClazz()
        self.assertEqual(
            str(clazz), "<class 'crawling_gocd.outputs.OutputCsv'>")

    def test_should_return_metrics_class(self):
        metricsClazz = self.parser.getMetrics()
        self.assertEqual(str(
            metricsClazz), "[<class 'crawling_gocd.four_key_metrics.DeploymentFrequency'>, <class 'crawling_gocd.four_key_metrics.ChangeFailPercentage'>]")
