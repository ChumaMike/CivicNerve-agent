# 🏙️ CivicNerve — The Autonomic Nervous System for Sustainable Cities

![Status](https://img.shields.io/badge/status-prototype-success)
![Stack](https://img.shields.io/badge/AI-IBM%20Granite%203.0-blue)
![Governance](https://img.shields.io/badge/governance-guardian%20active-green)

> Don't just detect the pothole. Write the work order, verify the budget, and schedule the crew — autonomously.

---

## 🚨 The Problem

Cities drown in broken infrastructure:
- **Slow response** — days for humans to read reports and dispatch crews
- **Safety risk** — excavations hitting gas lines due to human error
- **Citizen apathy** — people stop reporting because reports disappear into the void

---

## 💡 The Solution

CivicNerve is not a chatbot. It's an **agentic neural system** that automates the full lifecycle of city maintenance:

1. **Sees** — Granite Vision analyses citizen-submitted photos
2. **Thinks** — Granite 3.0 generates structured Work Orders from natural-language reports
3. **Protects** — A "Shift-Left" governance layer blocks unsafe or over-budget plans *before* execution
4. **Engages** — A gamified Civic Credits system rewards citizens for verified reports

---

## 🏗️ Architecture

Decoupled microservice design:

| Component | Tech | Function |
| :--- | :--- | :--- |
| Brain (Backend) | FastAPI · Pydantic | Logic, AI routing, strict type validation |
| Intelligence | IBM Granite + Mellea | Generative programming → structured Work Orders |
| Shield | Granite Guardian | Safety + budget governance layer |
| Citizen App | Streamlit | Report issues, track Civic Credits |
| City Ops Center | Streamlit | Dispatch crews, manage budgets |

---

## ⚡ Key Features

- **🛡️ Silent Review Loop** — Governance layer acts as a "Health Inspector," rejecting unsafe plans (e.g., "ignore safety rules") instantly
- **🎮 Civic Gamification** — Citizens earn Civic Credits; system detects duplicate reports to prevent spam
- **🧠 Context-Aware Priority** — Agent understands local context (treats water leaks as CRITICAL under drought conditions)

---

## 🚀 Run the Demo

Full ecosystem simulation across 3 terminal windows.

### 1. Neural Engine (Backend)

```bash
python -m src.api
```
Runs on `http://localhost:8000`

### 2. Citizen App

```bash
streamlit run src/citizen_app.py --server.port 8501
```
Runs on `http://localhost:8501`

### 3. City Ops Center

```bash
streamlit run src/city_ops.py --server.port 8502
```
Runs on `http://localhost:8502`

---

## 🗺️ Roadmap

- [ ] Real Granite Vision integration (currently simulated)
- [ ] WhatsApp report intake (piggyback off LinkUpGeo's Twilio layer)
- [ ] Deploy to a live municipality pilot
- [ ] Multi-language support (isiZulu, isiXhosa, Sesotho)

---

## License

MIT · Built by [Chuma Meyiswa](https://github.com/ChumaMike)
