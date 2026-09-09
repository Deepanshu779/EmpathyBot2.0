# 🧠 EmpathyBot 2.0 - Virtual Wellness Companion

A premium, highly-designed, interactive mental health and emotional support companion built with **Streamlit**, **Plotly**, and **Google Gemini AI**.

Styled with a dark glassmorphic UI, responsive micro-animations, customizable companion personas, real-time crisis detection, guided sensory grounding, and local-first mood data logging.

---

## 🌟 Premium Features

- **💬 Companion Chat**: Talk through your thoughts with three custom-designed, highly supportive virtual personas:
  - **🌿 Serene**: Quiet, soft, and soothing; ideal for anxiety and stress relief.
  - **⚡ Joy**: Radiant, optimistic, and validating; focuses on celebrating minor wins and self-compassion.
  - **🧠 Sage**: Reflective, wise, and analytical; leverages cognitive reframing (CBT) principles.
  - *Includes quick-starter chips, live sentiment tracking, chat export, and automated fallback to offline empathy rules.*
- **📊 Mood Journey & Analytics**: Record your emotional state, log contributing lifestyle factors (sleep, relationships, exercise, mindfulness), and view interactive wellness trends, average factor weights, and donut distribution charts using **Plotly**.
  - *Includes KPI metric cards, date timeframe filtering (7d, 30d, all-time), single-entry deletion, CSV export, and an instant "Load Sample Data" generator.*
- **🧘 Calm Zone & Mindfulness Studio**:
  - **Breathing Studio**: Interactive animated breathing visualizers with cycle timings for **Box Breathing (4-4-4-4)**, **Calming 4-7-8**, and **Coherent Rhythm (5-5)**.
  - **5-4-3-2-1 Sensory Grounding Tool**: Step-by-step checklist to de-escalate anxiety and panic by engaging sight, touch, sound, smell, and taste.
  - **Mindful Affirmations Deck**: Interactive affirmation draws categorized by anxiety relief, self-worth, courage, and evening sleep.
- **🚨 Crisis Safeguard & Helpline Directory**: Real-time keyword screening triggers empathetic boundaries and displays 24/7 confidential hotlines across **US**, **UK**, **India**, **Canada**, **Australia**, **Europe**, and **International** with direct clickable contact links.

---

## 🛠️ Technology Stack

- **Frontend/UI**: Python, Streamlit, HTML5/CSS3 (Glassmorphism, CSS keyframe animations)
- **Data & Visualizations**: Pandas, Plotly Express, Matplotlib
- **AI Core**: Google Gemini (`google-genai` & `google-generativeai`) with offline rule-based fallback
- **Testing**: Python `unittest` test suite

---

## 📂 Project Directory Structure

```
EmpathyBot2.0/
├── app.py                       # Main Landing Page / Quick Check-In / Navigation
├── requirements.txt             # Python Dependencies Specification
├── .env.example                 # Environment Variable Template
├── .streamlit/
│   └── config.toml              # Streamlit Dark Theme & Server Configurations
├── pages/                       # Multi-Page Modules
│   ├── 1_Chatbot.py             # Companion Chatbot Interface with Sentiment Badges
│   ├── 2_Mood_Tracker.py        # Interactive Mood Journeys, KPIs & Plotly Analytics
│   ├── 3_Helpline.py            # Comprehensive Regional Crisis Directory & Filter
│   └── 4_🧘_Calm_Zone.py        # Breathing Studio, 5-4-3-2-1 Grounding & Affirmations
├── utils/                       # Shared Backend & Engine Utilities
│   ├── bot_engine.py            # Gemini API connectors, offline rule engine & crisis check
│   ├── bot_logic.py             # Core routing and compatibility wrappers
│   ├── data_store.py            # Local CSV storage, sample data generator & CRUD
│   └── styles.py                # Glassmorphic CSS design system & animated breathing
├── tests/                       # Automated Test Suite
│   └── test_empathy_bot.py      # Unit tests for crisis, moods, store, and personas
└── README.md
```

---

## 🚀 How to Run Locally

### 1. Clone Repository & Install Dependencies
```bash
git clone https://github.com/Deepanshu779/EmpathyBot2.0.git
cd EmpathyBot2.0
pip install -r requirements.txt
```

### 2. (Optional) Configure Google Gemini API Key
To enable advanced AI mode, create a `.env` file or export your key:
```bash
cp .env.example .env
# Edit .env and set GEMINI_API_KEY=your_key_here
```
*Note: If no API key is provided, EmpathyBot operates in full Offline Empathy Engine mode.*

### 3. Launch the Application
Run the Streamlit server:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### 4. Run Automated Tests
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## ⚠️ Clinical Disclaimer
This application is designed as an emotional support, grounding, and self-reflection companion. It is **not a clinical diagnostic tool** and does not substitute for medical health advice, psychotherapy, or formal psychiatric care. If you are experiencing a crisis, navigate to the Crisis Helpline page and contact emergency services immediately.
