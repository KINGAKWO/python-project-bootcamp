# 🔢 Number Facts Analyzer

A Python-based data automation project that fetches, analyzes, and visualizes fun numerical facts from the [Numbers API](http://numbersapi.com/).  
Built as part of my **Python Developer Bootcamp – Phase II: Project Skill Consolidation** (Week 1 Project #2).

---

## 🚀 Features

- 🧮 **Data Collection:** Fetches number facts automatically from the Numbers API.  
- 📊 **Data Visualization:** Creates interactive trend plots and insights.  
- 📑 **Automated Reports:** Generates daily/weekly summaries using Python scripts.  
- 🌐 **Flask Dashboard:** Displays charts, reports, and an update button in a clean web interface.  
- 🔁 **Automation:** Scheduled updates through Python and cron/task schedulers.

---

## 🧠 Tech Stack

- **Language:** Python  
- **Libraries:** `requests`, `pandas`, `matplotlib`, `Flask`, `os`, `json`  
- **API:** Numbers API  
- **Automation:** Task Scheduler / cron  
- **Visualization:** Matplotlib charts  
- **Web Framework:** Flask  

---


---

## ⚡ How It Works

1. **Data Fetching** → Gets number facts via the Numbers API.  
2. **Data Visualization** → Generates summary plots (Matplotlib).  
3. **Automated Reporting** → Creates insights like “Most frequent number facts.”  
4. **Dashboard** → Flask app visualizes data and reports.  
5. **Automation** → Task scheduler runs updates automatically.  

---

## 🧩 Example Use

```bash
# Fetch new data
python main.py

# Generate report and chart
python generate_report.py && python generate_visuals.py

# Run Flask dashboard
python app.py

