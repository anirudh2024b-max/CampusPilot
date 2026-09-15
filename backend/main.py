from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import (
    SyllabusUploadRequest,
    PlanRequest,
    ReplanRequest,
    PlanResponse,
)

from agent import (
    call_llm_for_extraction,
    call_llm_for_planning,
    call_llm_for_replanning,
)

app = FastAPI(title="CampusPilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "CampusPilot backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/extract", response_model=dict)
def extract_syllabus(req: SyllabusUploadRequest):
    topics = call_llm_for_extraction(req.text)

    return {
        "topics": topics
    }


@app.post("/plan", response_model=PlanResponse)
def create_plan(req: PlanRequest):
    topics = call_llm_for_extraction(req.syllabus_text)

    if not topics:
        raise HTTPException(
            status_code=400,
            detail="No topics extracted from syllabus."
        )

    plan, explanation = call_llm_for_planning(
        topics,
        req.exam_date,
        req.hours_per_day
    )

    return PlanResponse(
        plan=plan,
        explanation=explanation
    )


@app.post("/replan", response_model=PlanResponse)
def replan(req: ReplanRequest):
    topics = call_llm_for_extraction(req.syllabus_text)

    if not topics:
        raise HTTPException(
            status_code=400,
            detail="No topics extracted from syllabus."
        )

    plan, explanation = call_llm_for_replanning(
        topics,
        req.exam_date,
        req.hours_per_day,
        req.completed_topics,
        req.missed_topics
    )

    return PlanResponse(
        plan=plan,
        explanation=explanation
    )