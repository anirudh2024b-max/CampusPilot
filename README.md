Inspiration:-

College students often receive syllabuses, assignments, and exam dates but struggle to convert them into a practical daily study plan. The problem is not only understanding what needs to be studied; it is deciding what to study first, how much time to allocate, and how to recover after missing a task.

As a student balancing academics and limited time, I wanted to build a focused tool that would turn an unstructured syllabus into a clear next action. This led to CampusPilot, an academic-action agent designed around planning and replanning rather than simple chat.

What it does
CampusPilot helps students create and adapt study plans.

The student provides:

Syllabus text.

An upcoming exam date.

The number of hours available for study each day.

CampusPilot then:

Extracts study topics from the syllabus.

Assigns planning priorities.

Generates a day-by-day study plan.

Shows estimated time for each task.

Tracks completed and missed topics.

Creates a revised plan based on the student’s progress.

The key behavior is adaptive replanning. If a student misses a task, CampusPilot does not leave them with an outdated schedule. It uses the updated progress to prioritize unfinished topics and create a new actionable plan.

How we built it
CampusPilot was built as a solo project using a Python FastAPI backend and a browser-based frontend.

The frontend uses:

HTML.

CSS.

JavaScript.

The JavaScript fetch API for communicating with the backend.

The backend uses:

Python.

FastAPI.

Uvicorn.

Pydantic models for request and response validation.


Direct Link to the project -
http://localhost:3000/


