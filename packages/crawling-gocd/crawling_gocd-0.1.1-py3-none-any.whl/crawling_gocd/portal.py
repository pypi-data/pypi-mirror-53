import os
from crawling_gocd.inputs_parser import InputsParser
from crawling_gocd.gocd_domain import Organization
from crawling_gocd.crawler import Crawler, CrawlingDataMapper
from crawling_gocd.calculator import Calculator
from crawling_gocd.four_key_metrics import DeploymentFrequency, ChangeFailPercentage, ChangeFailPercentage_ignoredContinuousFailed, MeanTimeToRestore

class Portal:
    def work(self):
        inputsParser = InputsParser("inputs.yaml")
        inputPipelines = inputsParser.parsePipelineConfig()
        inputMetricClazzList = inputsParser.getMetrics()
        inputCustomizeOutputClazz = inputsParser.outputCustomizeClazz()

        orgnization = Organization(
            os.environ["GOCD_SITE"], os.environ["GOCD_USER"], os.environ["GOCD_PASSWORD"])
        crawler = Crawler(orgnization)
        pipelineWithFullData = list(map(lambda pipeline: self.crawlingSinglePipeline(
            pipeline, crawler), inputPipelines))

        calculator = self.assembleCalculator(inputMetricClazzList)
        results = calculator.work(pipelineWithFullData, [])
        inputCustomizeOutputClazz().output(results)

    def crawlingSinglePipeline(self, pipeline, crawler):
        mapper = CrawlingDataMapper()
        histories = crawler.getPipelineHistories(
            pipeline.name, pipeline.calcConfig.startTime, pipeline.calcConfig.endTime)
        pipeline.histories = mapper.mapPipelineHistory(histories)
        return pipeline

    def assembleCalculator(self, metrics):
        handlers = list(map(lambda clazz: clazz(), metrics))
        return Calculator(handlers)
