# FinAdvisor AI — Personal Finance Advisor Bot

An AI-assisted personal finance web application built with **Python, Flask, SQLAlchemy, SQLite/PostgreSQL, JavaScript and optional Gemini AI**.

## Features

- Secure user registration and login
- Income tracking
- Expense tracking by category
- Spending analysis dashboard
- Budget guidance
- AI-powered financial recommendations
- Monthly financial reports
- Chart.js analytics
- SQLite for local development
- PostgreSQL-compatible configuration for production
- Render deployment configuration
- Optional Gemini API integration with a rule-based fallback

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- SQLite / PostgreSQL
- Jinja2
- HTML/CSS/Bootstrap
- JavaScript / Chart.js
- Gemini AI (optional)
- Gunicorn
- Render

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

Open `http://127.0.0.1:5000`.

## Gemini setup

Put your Gemini key in `.env`:

```env
GEMINI_API_KEY=your_key_here
```

The application still works without a key and uses a built-in educational recommendation engine.

## Deployment

This repository contains `render.yaml` for Render deployment.

1. Create a GitHub repository.
2. Push this project.
3. Create a new Web Service on Render.
4. Connect the GitHub repository.
5. Render reads the Python build/start commands from `render.yaml`.
6. Add `GEMINI_API_KEY` as a secret if AI generation is required.
7. After deployment, Render provides a public HTTPS URL for the demo.

## Project purpose

This project follows the supplied project brief: personal finance management, intelligent budgeting, expense tracking, spending analysis, savings planning, financial summaries, AI recommendations, database management, testing, and public deployment.

## Disclaimer

This is an educational software project. Financial suggestions are general information and are not a guarantee of investment returns or professional financial advice.
