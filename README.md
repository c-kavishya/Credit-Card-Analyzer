# 💳 Credit Card & Bank Statement Auditor

An AI-powered personal finance auditor built with **LangChain**, **Google Generative AI**, and **Streamlit**. 

The system utilizes a **two-stage LLM pipeline (sequential prompt chaining)** to parse raw, unstructured bank or credit card statements, isolate hidden financial leaks (dormant subscriptions, spending surges, penalty fees), and generate an actionable debt-reduction budget.

---

## 📌 Architecture Overview

Instead of executing extraction and financial advisory in a single prompt, the system breaks the workload into two deterministic stages to minimize hallucinations:


```

[Raw Statement Dump]
│
▼
┌────────────────────────────────────────────────────────┐
│ STAGE 1: Forensic Extraction & Classification          │
│ • System Persona: Forensic Financial Auditor           │
│ • Classifies transactions by category & expense type   │
│ • Tags anomalies: DORMANT_LEAK, SURGE, FEE_PENALTY     │
└────────────────────────┬───────────────────────────────┘
│ Structured Audit Context
▼
┌────────────────────────────────────────────────────────┐
│ STAGE 2: Prescriptive Financial Advisory               │
│ • System Persona: Personal Financial Counselor         │
│ • Generates plain-English financial health assessment  │
│ • Builds targeted subscription cut-list & 50/30/20 plan│
└────────────────────────┬───────────────────────────────┘
│
▼
[Streamlit Interactive Dual-Dashboard]

```

### Risk & Anomaly Tagging Legend
* **`DORMANT_LEAK`**: Inactive, forgotten, or auto-renewing subscriptions (e.g., gym memberships, streaming services).
* **`SURGE`**: Abnormally high discretionary spending spikes (e.g., dining, luxury purchases).
* **`FEE_PENALTY`**: Bank service charges, interest penalties, late fees, or maintenance costs.

---

## 🛠️ Tech Stack

* **Language:** Python
* **Orchestration:** LangChain (`langchain-google-genai`)
* **Foundation Models:** Google Gemini / Gemma (`gemma-4-31b-it`)
* **Frontend UI:** Streamlit
* **Environment Management:** `python-dotenv`

---

## 📁 Repository Structure

```text
├── credit_card_auditor.ipynb         # Prototyping notebook for the 2-stage pipeline
├── app.py                            # Streamlit web interface application
├── credit_card_expenses.txt          # Sample raw statement data for testing
├── .env.example                      # Environment variables template
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation

```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone [https://github.com/c-kavishya/Credit-Card-Analyzer.git](https://github.com/c-kavishya/Credit-Card-Analyzer.git)
cd Credit-Card-Analyzer

```

### 2. Set Up a Virtual Environment

```bash
python -m venv .venv
# On Windows PowerShell:
.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

*(Or install manually:)*

```bash
pip install streamlit langchain-google-genai python-dotenv

```

### 4. Configure API Keys

Create a `.env` file in the root directory and add your Google AI Studio API key:

```env
GEMINI_API_KEY="your_api_key_here"

```

---

## 💻 Usage

### Run the Web Dashboard

```bash
streamlit run app.py

```

### Run the Notebook Experimentation

Launch Jupyter Notebook or VS Code to run `credit_card_auditor.ipynb` step-by-step.

---

## 📝 Sample Input Format

You can paste plain unstructured lines into the application:

```text
05/01 Supermarket Groceries $112.40
05/02 Apple Services Recurring $9.99
05/04 DoorDash Food Delivery $48.20
05/06 Netflix 4K UHD $22.99
05/10 Anytime Fitness Gym $64.00
05/12 Late Payment Penalty Fee $39.00
05/25 Interest Charge Purchases $41.80
05/28 Luxury Restaurant Dinner $185.00




