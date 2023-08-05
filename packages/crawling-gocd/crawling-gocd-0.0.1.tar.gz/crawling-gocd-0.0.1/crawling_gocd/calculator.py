
class Calculator:
    def __init__(self, strategyHandlers):
        self.strategyHandlers = strategyHandlers

    def work(self, pipelines, results = []):
        for handler in self.strategyHandlers:
            handler.calculate(pipelines, results)
        return results


