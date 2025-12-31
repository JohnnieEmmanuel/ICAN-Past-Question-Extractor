
# ICAN Past Question Extractor

A Python tool that automatically extracts ICAN past question PDFs from the ICAN Pathfinder website (2018–N) and uploads them to a Supabase S3-compatible storage bucket. This project is designed to be **lossless, re-runnable, and duplicate-safe**.

---

## 🎯 What This Tool Does

* Scrapes past question PDFs from ICAN Pathfinder.
* Automatically categorizes files by exam year.
* Skips uploading files that already exist in Supabase storage.
* Uploads directly to a Supabase S3 bucket under `past_questions/{year}/`.

---

## 📁 Final Storage Structure

```
past_questions/
├── 2018/
├── 2019/
├── 2020/
├── 2021/
├── 2022/
├── 2023/
└── 2024/
```

---

## ⚙️ Requirements

* Python 3.9+
* Supabase project with **Storage enabled**
* Internet connection
* Environment variables for Supabase credentials

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/ican-study-material-ingestor.git
cd ican-study-material-ingestor
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

**Linux / macOS**

```bash
export SUPABASE_ACCESS_KEY="YOUR_SUPABASE_KEY"
export SUPABASE_SECRET_KEY="YOUR_SUPABASE_SECRET"
export SUPABASE_BUCKET_NAME="ican-study-texts"
```

**Windows (PowerShell)**

```powershell
setx SUPABASE_ACCESS_KEY "YOUR_SUPABASE_KEY"
setx SUPABASE_SECRET_KEY "YOUR_SUPABASE_SECRET"
setx SUPABASE_BUCKET_NAME "ican-study-texts"
```

Restart your terminal after setting them.

---

## ▶️ Usage

Run the extraction script:

```bash
python extract_past_questions.py
```

* Downloads PDFs from ICAN Pathfinder for 2018–2024.
* Saves them locally in `downloads/`.
* Uploads to Supabase storage under `past_questions/{year}/`.
* Skips files that already exist in the bucket.

---

## 🛡️ Safety & Best Practices

* Credentials are loaded via environment variables.
* Duplicate uploads are automatically prevented.
* Script is resilient to minor website changes.
* No past question PDFs are skipped — ever.

---

## ⚠️ Legal Notice

ICAN past questions are copyrighted content. This tool is intended for:

* Personal study systems
* Internal educational platforms
* Authorized distribution only

Ensure you have the appropriate rights before redistributing any materials publicly.

---

## 🚀 Possible Extensions

* Extract text from PDFs and store as searchable text.
* Rephrase questions using AI for practice apps.
* Async downloads for faster ingestion.
* Admin UI for reviewing uploaded PDFs.
* Cron / CI-based automatic ingestion.

---

## 🧑‍💻 Author

Built by **John Emmanuel ~ REDJOHN ~ CODEVIPER** for ICAN-focused learning platforms.

---
