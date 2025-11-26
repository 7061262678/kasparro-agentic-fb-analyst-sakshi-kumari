import numpy as np

class InsightAgent:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def generate(self, data_bundle):
        daily = data_bundle["daily"]

        # Not enough history → no insight
        if len(daily) < self.config["thresholds"]["min_days_for_trend"]:
            return []

        rwd = self.config["thresholds"]["recent_window_days"]
        swd = self.config["thresholds"]["reference_window_days"]

        recent = daily.tail(rwd)
        reference = daily.tail(rwd + swd).head(swd)

        rec_roas = recent["roas"].mean()
        ref_roas = reference["roas"].mean()
        delta = rec_roas - ref_roas

        # If ROAS hasn't changed enough, nothing to diagnose
        if abs(delta) < self.config["roas"]["roas_change_abs_threshold"]:
            return []

        hypotheses = []

        rec_ctr, ref_ctr = recent["ctr"].mean(), reference["ctr"].mean()
        rec_cvr, ref_cvr = recent["cvr"].mean(), reference["cvr"].mean()

        # Hypothesis — ROAS impacted by CTR drop
        if rec_ctr < ref_ctr:
            hypotheses.append({
                "id": "h_ctr",
                "title": "ROAS drop linked to declining CTR",
                "driver": "ctr",
                "delta": float(delta),
                "evidence": {
                    "recent_ctr": float(rec_ctr),
                    "reference_ctr": float(ref_ctr)
                }
            })

        # Hypothesis — ROAS impacted by CVR drop
        if rec_cvr < ref_cvr:
            hypotheses.append({
                "id": "h_cvr",
                "title": "ROAS drop linked to declining CVR",
                "driver": "cvr",
                "delta": float(delta),
                "evidence": {
                    "recent_cvr": float(rec_cvr),
                    "reference_cvr": float(ref_cvr)
                }
            })

        # If neither CTR nor CVR is strongly directional
        if not hypotheses:
            hypotheses.append({
                "id": "h_mixed",
                "title": "ROAS variation driven by mixed CTR/CVR factors",
                "driver": "mixed",
                "delta": float(delta),
                "evidence": {}
            })

        self.logger.log("insights", {"count": len(hypotheses)})
        return hypotheses
