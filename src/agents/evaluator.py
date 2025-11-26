class EvaluatorAgent:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def evaluate(self, hypotheses):
        evaluated = []
        threshold = self.config["roas"]["roas_change_abs_threshold"]

        for h in hypotheses:
            delta = abs(h["delta"])
            # Confidence score = how strong the ROAS change is relative to threshold
            confidence = min(1.0, delta / (2 * threshold))
            confidence = round(confidence, 2)

            evaluated.append({
                "id": h["id"],
                "title": h["title"],
                "driver": h["driver"],
                "confidence": confidence,
                "evidence": h["evidence"]
            })

        self.logger.log("evaluated_hypotheses", {"count": len(evaluated)})
        return evaluated
