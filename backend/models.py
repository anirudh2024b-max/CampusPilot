from pydantic import BaseModel
from typing import List, Optional

class SyllabusUploadRequest(BaseModel):
    text: str  # For MVP, you paste syllabus text; later you can add PDF parsing

class PlanRequest(BaseModel):
    syllabus_text: str
    exam_date: str  # e.g. "2026-09-20"
    hours_per_day: int

class Task(BaseModel):
    day: int
    topic: str
    estimated_hours: float
    priority: str  # "high", "medium", "low"
    done: bool = False

class PlanResponse(BaseModel):
    plan: List[Task]
    explanation: str

class ReplanRequest(BaseModel):
    syllabus_text: str
    exam_date: str
    hours_per_day: int
    completed_topics: List[str]
    missed_topics: List[str]