# AI Business Analytics Dashboard

An interactive, cloud-deployed Business Intelligence (BI) dashboard built with **Streamlit**, **Pandas**, and **Plotly**, integrated with **Groq API (LLM)** to automate sales performance analysis and instantly generate executive business reports.

🔗 **Live Demo:** [View the Dashboard](https://ai-business-analytics-dashboard-fabkcr8dqhz49jy6xjrqoo.streamlit.app/)

---

## 📊 Project Overview & Architecture

This project demonstrates an end-to-end data analytics workflow, divided into two main stages:

1. **Data Extraction & Pipeline (`data_extraction.ipynb`):** A Google Colab notebook utilizing SQL queries within Google BigQuery to extract raw sales and web-analytics data, clean it, and export it into a structured CSV file.
2. **BI & AI Automation Dashboard (`app.py`):** A web application that visualizes key business metrics (Revenue, Conversion Rate, Top Products) and leverages an LLM to generate an automated Executive Report for management.

---

## 🛠️ Tech Stack

* **Data Extraction & Processing:** SQL (BigQuery), Python, Pandas, Google Colab
* **Data Visualization:** Plotly Express
* **Web Framework:** Streamlit
* **AI Integration:** Groq API / OpenAI SDK (LLM-driven automated insight generation)
* **Deployment:** Streamlit Community Cloud

---

## 📸 Screenshots

### 1. Main Page (Upload a CSV file to launch the dashboard)
<img width="1667" height="426" alt="image" src="https://github.com/user-attachments/assets/072f79f9-4f39-406f-8bcd-282764168340" />


### 2. BI Dashboard
<img width="2421" height="1105" alt="image" src="https://github.com/user-attachments/assets/78d9a427-4e3b-4f1c-8d68-8c48a346a694" />

### 3. AI-Generated Report
<img width="2391" height="1284" alt="image" src="https://github.com/user-attachments/assets/3bf03322-5956-4943-bc36-318de9664272" />
