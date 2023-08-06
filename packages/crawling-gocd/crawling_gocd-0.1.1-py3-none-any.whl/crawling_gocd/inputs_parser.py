import yaml
import datetime
import sys
from crawling_gocd.gocd_domain import Pipeline
from crawling_gocd.calculate_domain import InputsCalcConfig


class InputsParser:
    def __init__(self, filePath):
        with open(filePath, 'r') as stream:
            try:
                self.inputs = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print("yaml file read failed, {}", exc)

    def parsePipelineConfig(self):
        globalStartTime = self.inputs.get("global", {}).get(
            "start_time", datetime.datetime(1970, 1, 1))
        globalEndTime = self.inputs.get("global", {}).get(
            "end_time", datetime.datetime.now())

        return list(map(lambda pipeline: self.mapSingle(
            pipeline, globalStartTime, globalEndTime), self.inputs["pipelines"]))

    def mapSingle(self, pipelineConfig, globalStartTime, globalEndTime):
        inputCalcConfig = InputsCalcConfig(pipelineConfig["calc_grouped_stages"], pipelineConfig.get(
            "startTime", globalStartTime), pipelineConfig.get("endTime", globalEndTime))
        return Pipeline(pipelineConfig["name"], inputCalcConfig)

    def outputCustomizeClazz(self):
        absoluteClassName = self.inputs.get("output_class_name", None)
        if absoluteClassName == None:
            return getattr(sys.modules["crawling_gocd.outputs"], "OutputCsv")

        partitions = absoluteClassName.rpartition(".")
        return getattr(sys.modules[partitions[0]], partitions[2]) 
        
    def getMetrics(self):
        metrics = self.inputs["metrics"]
        four_key_metrics = metrics.get("four_key_metrics", [])
        return list(map(lambda m: getattr(sys.modules["crawling_gocd.four_key_metrics"], m), four_key_metrics))
             
        
        
