import sys
import yaml
from src.orchestrator.pipeline import AnalysisPipeline

def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python run.py "Analyze ROAS drop"')
        sys.exit()

    user_query = sys.argv[1]
    config = load_config("config/config.yaml")

    pipeline = AnalysisPipeline(config)
    pipeline.run(user_query)
