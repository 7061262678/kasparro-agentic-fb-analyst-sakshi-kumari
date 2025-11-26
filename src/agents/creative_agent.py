import random

class CreativeAgent:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        random.seed(config.get("seed", 42))

    def generate(self, data_bundle):
        df = data_bundle["raw"]
        threshold_ctr = self.config["thresholds"]["low_ctr"]
        low_ctr_df = df[df["ctr"] < threshold_ctr]

        if low_ctr_df.empty:
            self.logger.log("creative_recos", {"count": 0})
            return []

        recos = []

        for (campaign, adset), g in low_ctr_df.groupby(["campaign_name", "adset_name"]):
            messages = g["creative_message"].dropna().astype(str).tolist()
            sample_msg = messages[0] if messages else ""

            idea = self._build_idea(campaign, sample_msg)

            recos.append({
                "campaign": campaign,
                "adset": adset,
                "current_ctr": float(g["ctr"].mean()),
                "sample_message": sample_msg,
                **idea
            })

        self.logger.log("creative_recos", {"count": len(recos)})
        return recos

    def _build_idea(self, campaign, sample_msg):
        # Study current creative message to decide angle
        if "free" in sample_msg.lower():
            angle = "urgency"
        elif "discount" in sample_msg.lower():
            angle = "benefit"
        else:
            angle = random.choice(["social_proof", "benefit", "urgency"])

        if angle == "social_proof":
            return {
                "suggest_headline": f"Why customers trust {campaign}",
                "suggest_body": f"Feature top reviews, transformation stories, and real results. Reference: {sample_msg[:100]}",
                "cta": "See customer stories"
            }
        elif angle == "urgency":
            return {
                "suggest_headline": f"Limited time — grab {campaign} before the offer ends",
                "suggest_body": f"Highlight scarcity and time-bound offer. Reference: {sample_msg[:100]}",
                "cta": "Claim the offer"
            }
        else:  # benefit angle
            return {
                "suggest_headline": f"Upgrade your everyday experience with {campaign}",
                "suggest_body": f"Focus on comfort, savings, and practicality. Reference: {sample_msg[:100]}",
                "cta": "Shop now"
            }
