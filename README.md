
# CampusPilot

An adaptive academic-action agent that turns syllabuses into realistic study plans.

## Overview

CampusPilot is a prototype academic-action agent for college students. It converts syllabus text into structured study topics, generates a prioritized study plan based on an exam date and available study hours, and replans the schedule when tasks are completed or missed.

## Problem

College students often have syllabuses, assignments, and examination deadlines but struggle to turn them into realistic daily actions.

The difficulty is not only knowing what to study. Students also need to decide:

- Which topics should be studied first.
- How much time to spend on each topic.
- How to fit study tasks around limited availability.
- How to recover after missing a planned task.

Traditional to-do lists do not understand academic topics or automatically adapt to changing progress.

## Solution

CampusPilot provides a focused workflow:

1. Accept syllabus text.
2. Extract study topics.
3. Assign planning priorities.
4. Generate a day-by-day study plan.
5. Track completed and missed topics.
6. Generate a revised plan based on progress.

The key feature is adaptive replanning. The plan changes when the student's situation changes.

## Features

- Syllabus topic extraction.
- Topic priority assignment.
- Exam-date-based planning.
- Available-hours-based scheduling.
- Estimated study duration.
- Progress tracking.
- Missed-task replanning.
- Browser-based interface.
- FastAPI backend with REST endpoints.

## Demo workflow

```text
Paste syllabus
      ↓
Extract topics
      ↓
Enter exam date and available hours
      ↓
Generate study plan
      ↓
Mark tasks completed or missed
      ↓
Generate revised plan
```

## Technology stack

### Frontend

- HTML
- CSS
- JavaScript
- JavaScript Fetch API

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic

## Project structure

```text
campus-pilot/
├── README.md
├── .gitignore
├── backend/
│   ├── agent.py
│   ├── main.py
│   └── models.py
└── frontend/
    ├── app.js
    ├── index.html
    └── styles.css
```

## How to run locally

### Requirements

Install:

- Python 3.10 or newer.
- Git.
- A modern web browser.

### 1. Clone the repository

```bash
git clone [https://github.com/YOUR-USERNAME/campus-pilot.git](https://github.com/YOUR-USERNAME/campus-pilot.git)
cd campus-pilot
```

### 2. Create the Python environment

Open a terminal in the backend folder:

```bash
cd backend
python -m venv .venv
```

### 3. Activate the environment

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

#### Windows Command Prompt

```cmd
.venv\Scripts\activate.bat
```

#### macOS/Linux

```bash
source .venv/bin/activate
```

### 4. Install backend dependencies

```bash
pip install fastapi "uvicorn[standard]" python-multipart pydantic
```

### 5. Start the backend

Run this command while inside the `backend` folder:

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8001
```

The backend will run at:

```text
http://127.0.0.1:8001
```

API documentation is available at:

```text
http://127.0.0.1:8001/docs
```

### 6. Start the frontend

Open a second terminal.

From the project root, run:

```bash
cd frontend
python -m http.server 3000
```

Open the application at:

```text
http://localhost:3000
```

Keep both terminals running while using the application.

## API endpoints

### `GET /`

Checks that the backend is running.

### `GET /health`

Returns the backend health status.

### `POST /extract`

Extracts structured study topics from syllabus text.

Example request:

```json
{
  "text": "Unit 1: Arrays and Strings\nUnit 2: Linked Lists\nUnit 3: Trees"
}
```

### `POST /plan`

Generates a study plan using syllabus text, exam date, and available hours.

Example request:

```json
{
  "syllabus_text": "Unit 1: Arrays\nUnit 2: Linked Lists\nUnit 3: Trees",
  "exam_date": "2026-09-20",
  "hours_per_day": 3
}
```

### `POST /replan`

Generates a revised plan using completed and missed topics.

Example request:

```json
{
  "syllabus_text": "Unit 1: Arrays\nUnit 2: Linked Lists\nUnit 3: Trees",
  "exam_date": "2026-09-20",
  "hours_per_day": 3,
  "completed_topics": ["Arrays"],
  "missed_topics": ["Linked Lists", "Trees"]
}
```

## Agent workflow

CampusPilot separates the workflow into three stages:

```text
Extraction stage
    ↓
Planning stage
    ↓
Replanning stage
```

The extraction stage identifies topics from syllabus text.

The planning stage creates a schedule based on topic priority, exam date, and available time.

The replanning stage uses student progress to prioritize unfinished topics and generate a revised schedule.

## AI and development approach

This project was developed using AI-assisted programming tools for code scaffolding, debugging, documentation, and implementation support.

The current prototype demonstrates the agentic workflow using structured and deterministic planning logic so that the result is reliable and reproducible. The architecture is designed to support a model-backed AI extraction and personalization layer in future versions.

The final product workflow, integration, testing, and implementation decisions were reviewed by the project author.

## Current limitations

- The MVP accepts pasted syllabus text rather than PDF uploads.
- The prototype uses lightweight structured planning logic.
- Data is not persisted after the backend restarts.
- Authentication is not included.
- Calendar integration is not included.
- The application is currently intended as a local prototype.
- The current planner is not intended for medical, legal, or safety-critical decisions.

## Future roadmap

- PDF syllabus and assignment uploads.
- LLM-backed topic extraction.
- Retrieval from lecture notes and course materials.
- Quiz and flashcard generation.
- Persistent user accounts and progress history.
- Calendar integration.
- Notifications and reminders.
- Tamil-English language support.
- Weak-topic analytics.
- Personalized planning based on performance and learning speed.

## Demo

Demo video:

PASTE-YOUR-DEMO-VIDEO-LINK-HERE

Repository:

https://github.com/YOUR-USERNAME/campus-pilot

## License

This project is released under the MIT License.

