from openai import OpenAI

from config import GROQ_API_KEY, GROQ_MODEL
from metrics import SalesMetrics


def generate_ai_report(metrics: SalesMetrics) -> str:
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set. Add your key to the .env file.")

    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=GROQ_API_KEY,
    )

    prompt = f"""
You are a Senior Business Intelligence Analyst preparing an executive report for company management.
Based ONLY on the sales metrics provided below, write a professional business report in English (maximum 400 words).

Structure your report into the following sections:
## 1. Business Strengths
## 2. Business Risks
## 3. Key Trends & Customer Behaviour
## 4. Strategic Recommendations

Sales Metrics:
{metrics.to_kpi_text()}
"""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        timeout=60.0,
    )

    return response.choices[0].message.content or ""
