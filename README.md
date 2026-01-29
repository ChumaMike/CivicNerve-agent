# 🏙️ CivicNerve: The Sentient City Operating System
> **Winner: [Hackathon Name] Submission** > *A Self-Healing, Governed AI Agent for Sustainable City Infrastructure.*

![Status](https://img.shields.io/badge/Status-Prototype_Live-success)
![Stack](https://img.shields.io/badge/AI-IBM_Granite_3.0-blue)
![Governance](https://img.shields.io/badge/Governance-Guardian_Active-green)

## 🚨 The Problem
Cities are drowning in broken infrastructure.
1.  **Slow Response:** It takes days for a human to read a report and assign a crew.
2.  **Safety Risks:** Human error leads to dangerous excavations (e.g., hitting gas lines).
3.  **Citizen Apathy:** People stop reporting issues because they feel ignored.

## 💡 The Solution: CivicNerve
CivicNerve is not a chatbot; it is an **Agentic Neural System**. It automates the entire lifecycle of city maintenance:
1.  **Sees:** Uses **Granite Vision** (Simulated) to analyze citizen photos.
2.  **Thinks:** Uses **Granite 3.0** to generate technical Work Orders from natural language.
3.  **Protects:** A **"Shift-Left" Governance Layer** blocks unsafe or over-budget plans *before* execution.
4.  **Engages:** A **Gamified Wallet System** rewards citizens for being the city's eyes.

---

## 🏗️ Architecture
CivicNerve is built on a decoupled **Microservice Architecture**:

| Component | Tech Stack | Function |
| :--- | :--- | :--- |
| **The Brain (Backend)** | `FastAPI` + `Pydantic` | Handles logic, AI routing, and strict type validation. |
| **The Intelligence** | `IBM Granite` + `Mellea` | Generative programming to create structured Work Orders. |
| **The Shield** | `Granite Guardian` | Governance layer to audit safety and budget compliance. |
| **Citizen App** | `Streamlit` | Frontend for reporting issues and tracking Rewards/Credits. |
| **City Ops Center** | `Streamlit` | Secure dashboard for dispatching crews and managing budgets. |

---

## ⚡ Key Features (The "Wow" Factors)
* **🛡️ Silent Review Loop:** The AI generates a plan, but the Governance Layer acts as a "Health Inspector," rejecting unsafe plans (e.g., "Ignore safety rules") instantly.
* **🎮 Civic Gamification:** Citizens earn **"Civic Credits"** for verified reports. The system intelligently detects duplicates to prevent spam.
* **🧠 Context-Aware Priority:** The Agent understands local context (e.g., treating "Water Leaks" as CRITICAL due to drought conditions).

---

## 🚀 How to Run the Demo (The Ecosystem)
This project simulates a full city ecosystem using **3 Terminal Windows**.

### 1. Start the Neural Engine (Backend)
```bash
python -m src.api
Runs on: http://localhost:8000

2. Start the Citizen App (Frontend A)
Bash

streamlit run src/citizen_app.py --server.port 8501
Runs on: http://localhost:8501

3. Start the City Ops Center (Frontend B)
Bash

streamlit run src/city_ops.py --server.port 8502
Runs on: http://localhost:8502