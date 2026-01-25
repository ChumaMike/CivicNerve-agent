# 🏙️ CivicNerve: The Sentient City Infrastructure Twin

> **IBM TechXchange Hackathon 2026 Entry** > *Track: AI Automation / Sustainable Cities*

CivicNerve is an autonomous **Agentic AI** system designed to maintain city infrastructure. It ingests legacy engineering blueprints, analyzes citizen reports (text & vision), and autonomously generates strictly governed work orders.

It moves beyond simple chatbots by implementing **Self-Healing Loops** and **Shift-Left Governance**.

---



## 🛠️ The Winning Arsenal (Tech Stack)

We utilize the **2026 IBM AI Stack** to ensure reliability and trust:

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Brain** | **CUGA** (via LangGraph) | Planner-Executor engine for complex decision making. |
| **Motor** | **Mellea** (Generative Programming) | Generates structured, type-safe SQL & JSON outputs (no hallucinations). |
| **Senses** | **Docling** | Ingests complex PDF blueprints and engineering schematics. |
| **Vision** | **IBM Granite 3.0 Vision** | Analyzes photos of infrastructure damage. |
| **Safety** | **ALTK & Granite Guardian** | "Silent Review" loops to validate budget & safety before execution. |
| **Security** | **IBM Bob** | Scaffolding and vulnerability scanning. |

---

## 🏗️ Architecture: The "Three-Lobe" Brain

1.  **Sensory Cortex (Ingestion):** Docling parses 50-year-old pipe schematics into vector-searchable knowledge.
2.  **Frontal Lobe (Reasoning):** The Agent plans a response: *Analyze Hazard -> Check Budget -> Schedule Crew*.
3.  **Guardian Lobe (Governance):** ALTK intercepts the final plan. If the AI suggests a $1M repair for a pothole, the Guardian blocks it and forces a replan.

---

## 🚀 Quick Start

### 1. Prerequisites
* Python 3.11+
* IBM Cloud API Key (for Watsonx.ai)

### 2. Installation
```bash
git clone [https://github.com/your-username/civic-nerve.git](https://github.com/your-username/civic-nerve.git)
cd civic-nerve
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt