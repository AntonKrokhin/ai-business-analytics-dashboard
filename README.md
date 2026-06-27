# AI Report Generator — BI Dashboard

CSV → Python → Streamlit → AI → Dashboard

## Features

- Upload a sales CSV file
- KPI cards and Plotly charts
- AI report via Groq API with download support

## Quick Start

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

copy .env.example .env
# Add your GROQ_API_KEY to .env

streamlit run app.py
```

## Project Structure

```
app.py        # Streamlit UI
metrics.py    # Pandas aggregations
ai_report.py  # Groq AI report
config.py     # Environment variables
```

## Environment Variables (.env)

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Groq API key |
| `GROQ_MODEL` | Model name (default: `llama-3.1-8b-instant`) |
