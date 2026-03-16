# SAT Score Tracker

A full-stack web app to track SAT practice test scores, visualize progress, and get AI-powered coaching feedback.

## Features
- Log Math and Reading & Writing section scores separately
- Live score trajectory chart with trend detection
- AI coaching feedback via OpenAI API (GPT-4o-mini)
- Score prediction using linear regression
- Test date countdown timer
- Persistent local storage via JSON

## Tech Stack
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript, Chart.js
- **AI:** OpenAI API (GPT-4o-mini)

## Setup
1. Clone the repository
```bash
   git clone https://github.com/YOUR_USERNAME/sat-tracker.git
   cd sat-tracker
```
2. Install dependencies
```bash
   pip install -r requirements.txt
```
3. Run the app
```bash
   python app.py
```
4. Open `http://localhost:5000` in your browser

## AI Coaching (Optional)
Paste your OpenAI API key into the field at the top of the app. It's never stored — only used per request.