from typing import List, Dict, Any
from models import Task
import json
from datetime import datetime, timedelta

# -------------------------
# LLM CALL (PLACEHOLDER)
# -------------------------
# In real version, call your LLM API here and parse JSON.
# For hackathon demo, we simulate structured output.

def call_llm_for_extraction(syllabus_text: str):
    lines = [
        line.strip()
        for line in syllabus_text.splitlines()
        if line.strip()
    ]

    topics = []

    for index, line in enumerate(lines):
        lower_line = line.lower()

        if lower_line.startswith("unit"):
            if ":" in line:
                topic_name = line.split(":", 1)[1].strip()
            else:
                topic_name = line

            topics.append({
                "topic": topic_name,
                "weight": 3 if index <= 2 else 2
            })

    if not topics:
        for line in lines:
            if len(line) > 3:
                topics.append({
                    "topic": line,
                    "weight": 1
                })

    return topics[:20]


def call_llm_for_planning(topics: List[Dict[str, Any]], exam_date: str, hours_per_day: int) -> tuple[List[Task], str]:
    """
    Given extracted topics, exam date, and daily hours, produce a plan.
    Returns (list of Task, explanation string).
    """
    # Simple heuristic planner:
    # - Spread topics over days until exam
    # - Higher weight topics get more hours / earlier days
    
    today = datetime.now()
    exam = datetime.strptime(exam_date, "%Y-%m-%d")
    days_available = max(1, (exam - today).days)
    
    # Sort topics by weight descending
    sorted_topics = sorted(topics, key=lambda t: t["weight"], reverse=True)
    
    plan: List[Task] = []
    day = 1
    topic_idx = 0
    
    while day <= days_available and topic_idx < len(sorted_topics):
        t = sorted_topics[topic_idx]
        # higher weight => more hours
        base_hours = 1.0
        hours = base_hours + (t["weight"] - 1) * 0.5
        hours = min(hours, hours_per_day)  # don't exceed daily limit
        
        task = Task(
            day=day,
            topic=t["topic"],
            estimated_hours=round(hours, 1),
            priority="high" if t["weight"] >= 3 else ("medium" if t["weight"] == 2 else "low"),
            done=False
        )
        plan.append(task)
        
        # If we still have hours left today, maybe add another small topic
        used_today = sum(p.estimated_hours for p in plan if p.day == day)
        if used_today + 1.0 <= hours_per_day:
            # try to add next topic same day if small
            if topic_idx + 1 < len(sorted_topics):
                topic_idx += 1
                continue
        
        day += 1
        topic_idx += 1
    
    explanation = (
        f"Plan created for exam on {exam_date} with {hours_per_day} hours/day. "
        "Higher-weight topics are scheduled earlier. If you miss tasks, ask for replanning."
    )
    return plan, explanation


def call_llm_for_replanning(
    topics: List[Dict[str, Any]],
    exam_date: str,
    hours_per_day: int,
    completed_topics: List[str],
    missed_topics: List[str]
) -> tuple[List[Task], str]:
    """
    Replan given completed and missed topics.
    For MVP, we just push missed topics earlier and mark completed as done.
    """
    # Reuse basic planner but prioritize missed topics
    missed_set = set(missed_topics)
    completed_set = set(completed_topics)
    
    # Build topic list with boosted weight for missed
    enriched = []
    for t in topics:
        topic_name = t["topic"]
        weight = t["weight"]
        if topic_name in missed_set:
            weight = 4  # boost
        enriched.append({"topic": topic_name, "weight": weight})
    
    plan, base_explanation = call_llm_for_planning(enriched, exam_date, hours_per_day)
    
    # Mark completed as done
    for task in plan:
        if task.topic in completed_set:
            task.done = True
            task.priority = "low"
    
    explanation = (
        base_explanation +
        " This is a revised plan: missed topics are prioritized; completed topics are marked done."
    )
    return plan, explanation