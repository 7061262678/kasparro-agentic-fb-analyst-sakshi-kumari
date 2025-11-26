class PlannerAgent:
    def __init__(self, config):
        self.config = config

    def plan(self, query: str) -> dict:
        q = query.lower()
        diagnose = any(x in q for x in ["roas", "performance", "drop", "analyze", "why"])
        creative = any(x in q for x in ["creative", "ctr", "headlines", "copy"])
        if not diagnose and not creative:
            diagnose = creative = True
        return {"diagnose": diagnose, "creative": creative}
