from pathlib import Path
import json
from src.agents.planner import PlannerAgent
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator import EvaluatorAgent
from src.agents.creative_agent import CreativeAgent
from src.utils.logger import SimpleLogger

class AnalysisPipeline:
    def __init__(self, config):
        self.config = config
        Path(config["paths"]["logs_dir"]).mkdir(exist_ok=True)
        log_file = Path(config["paths"]["logs_dir"]) / "run.jsonl"
        self.logger = SimpleLogger(log_file)

    def run(self, user_query):
        self.logger.log("query_received", {"query": user_query})

        # Stage 1 — Planner
        planner = PlannerAgent(self.config)
        plan = planner.plan(user_query)
        self.logger.log("planner_output", plan)

        # Stage 2 — Data
        data_agent = DataAgent(self.config, self.logger)
        df = data_agent.load_and_aggregate()

        # Stage 3 — Insights & Evaluation
        hypotheses = []
        if plan.get("diagnose", False):
            insight_agent = InsightAgent(self.config, self.logger)
            hypotheses = insight_agent.generate(df)

            evaluator = EvaluatorAgent(self.config, self.logger)
            hypotheses = evaluator.evaluate(hypotheses)

            Path(self.config["paths"]["insights_json"]).write_text(
                json.dumps(hypotheses, indent=2), encoding="utf-8"
            )
            self.logger.log("insights_generated", hypotheses)

        # Stage 4 — Creative Suggestions
        creatives = []
        if plan.get("creative", False):
            creative_agent = CreativeAgent(self.config, self.logger)
            creatives = creative_agent.generate(df)

            Path(self.config["paths"]["creatives_json"]).write_text(
                json.dumps(creatives, indent=2), encoding="utf-8"
            )
            self.logger.log("creatives_generated", creatives)

        # Final stage — Human readable report
        self._write_report(hypotheses, creatives)
        self.logger.log(
            "pipeline_complete",
            {"hypotheses_count": len(hypotheses), "creatives_count": len(creatives)}
        )

    def _write_report(self, hypotheses, creatives):
        report = ["# Facebook ROAS Diagnostic Report\n"]

        report.append("## Insights\n")
        if hypotheses:
            for h in hypotheses:
                report.append(f"- {h['title']} (confidence: {h['confidence']})")
        else:
            report.append("- No ROAS drivers identified.\n")

        report.append("\n## Creative Recommendations\n")
        if creatives:
            for c in creatives:
                report.append(f"### {c['campaign']} — {c['adset']}")
                report.append(f"- CTR: {c['current_ctr']}")
                report.append(f"- Headline: {c['suggest_headline']}")
                report.append(f"- Body: {c['suggest_body']}")
                report.append(f"- CTA: {c['cta']}\n")
        else:
            report.append("- No creatives flagged as underperforming.\n")

        Path(self.config["paths"]["report_md"]).write_text(
            "\n".join(report), encoding="utf-8"
        )
