from fastapi import FastAPI

from combinations.generator import generate_combinations
from config import API_KEY
from schemas import GenerationResult, ScheduleRequest, Section
from uwaterloo.client import fetch_sections
from uwaterloo.course_code import parse_course_code
from uwaterloo.term_code import term_code

app = FastAPI()


@app.post("/api/schedules", response_model=GenerationResult)
def generate_schedules(request: ScheduleRequest) -> GenerationResult:
    """Generate all valid, conflict-free schedule combinations for the requested courses.

    Args:
        request: Term and the raw course code strings to include.

    Returns:
        GenerationResult with every valid combination found.
    """
    term = term_code(request.term)

    sections: list[Section] = []
    for code in request.courses:
        course_code = parse_course_code(code)
        sections.extend(fetch_sections(course_code, term, API_KEY))

    return generate_combinations(sections)
