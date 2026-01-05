# 🏥 Healthcare Synthetic Data Generator

A Python tool designed to generate realistic, anonymized healthcare datasets for testing SaaS applications, BI dashboards (like J-Vision), and ERP systems.

## 🚀 Features
- Generates **GDPR-proof** synthetic data (no real patient info).
- Creates related datasets: **Patients** → **Care Episodes** → **Activities**.
- **Smart Logic**: Ensures treatments always fall within valid care episode dates.
- **Dutch Localization**: Uses `faker` with `nl_NL` for realistic Dutch names and cities.

## 🛠️ Usage
1. Install requirements: `pip install -r requirements.txt`
2. Run the script: `python main.py`
3. Find your CSV exports in the `/output` folder.

## 📊 Use Case
Originally developed to populate **J-Vision**, a healthcare BI dashboard, with test data to demonstrate financial production analysis without compromising patient privacy.
