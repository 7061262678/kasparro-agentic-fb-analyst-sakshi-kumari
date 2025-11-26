from src.agents.evaluator import EvaluatorAgent

config = {
    "roas": {
        "roas_change_abs_threshold": 0.2
    }
}

class DummyLogger:
    def log(self, *args, **kwargs):
        pass

def test_evaluator_confidence_range():
    logger = DummyLogger()
    evaluator = EvaluatorAgent(config, logger)

    hypotheses = [{"id": "h1", "title": "test", "driver": "ctr", "delta": 0.5, "evidence": {}}]
    output = evaluator.evaluate(hypotheses)

    assert 0 <= output[0]["confidence"] <= 1
