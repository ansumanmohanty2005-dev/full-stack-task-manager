# TaskFlow — Full-Stack Task Manager

A portfolio-ready full-stack web application demonstrating a responsive frontend, Python/Flask backend, REST API endpoints, CRUD operations and SQLite persistence.

## Tech Stack
HTML5, CSS3, JavaScript, Python, Flask, SQLite, REST API

## Features
- Create tasks with title, description and priority
- View all, pending or completed tasks
- Mark tasks complete/pending
- Delete tasks
- Persistent SQLite database
- Responsive interface

## Run locally
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5000`.

## GitHub
```bash
git init
git add .
git commit -m "Build full-stack task manager"
git branch -M main
git remote add origin YOUR_REPOSITORY_URL
git push -u origin main
```
