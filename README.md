# Kasparro — Agentic Facebook Performance Analyst

This project implements an agentic system that diagnoses Facebook Ads performance.
It identifies why ROAS changes over time and recommends new creative ideas for
low-CTR campaigns using both quantitative signals and creative messaging patterns.
(Self-review PR temporary note — will be removed after merge)
This line is added only for the self-review PR.

---

##  Quick Start

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py "Analyze ROAS drop"

---

## Autonomous Agentic Facebook Performance Analyst

### Project Overview
This system autonomously analyzes Facebook Ads performance and explains **why ROAS changed**, **what caused the change**, and **how to improve creatives**.

The pipeline includes 5 collaborating agents:

| Agent           | Role                                           |
|----------------|-------------------------------------------------|
| Planner Agent  | Breaks the marketing question into subtasks     |
| Data Agent     | Loads & aggregates the dataset                  |
| Insight Agent  | Generates ROAS-related hypotheses               |
| Evaluator Agent| Scores hypotheses with quantitative confidence  |
| Creative Agent | Suggests ad copy for low-CTR campaigns          |

**Outputs written by the pipeline:**

- `reports/insights.json`
- `reports/creatives.json`
- `reports/report.md`
- `logs/run.jsonl`

---

## Run The Project

```bash
pip install -r requirements.txt
python run.py "Analyze ROAS drop"
python run.py "creative ideas for ads"


---

## 🛠 Tech Stack & Skills (Kasparro Project)

| Category | Tools / Skills |
|----------|----------------|
| Programming | Python |
| AI / ML | Applied AI • Prompt Engineering • Agent Reasoning |
| Data Work | Pandas • CSV • Insights & Hypothesis Scoring |
| Architecture | Multi-Agent Pipeline • Orchestrator Model |
| Output | JSON • Markdown Reports • Trace Logging |

" " 
