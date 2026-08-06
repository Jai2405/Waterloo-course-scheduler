from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from combinations.generator import generate_combinations
from config import API_KEY
from schemas import CourseError, GenerationResult, ScheduleRequest, Section
from uwaterloo.client import CourseNotFoundError, fetch_sections
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

    Raises:
        HTTPException: 400, if one or more requested courses are invalid, not
            found, or have no sections offered this term. Every bad course is
            reported at once, not just the first one found.
    """
    term = term_code(request.term)
    term_label = f"{request.term.term} {request.term.year}"

    sections: list[Section] = []
    errors: list[CourseError] = []

    for code in request.courses:
        try:
            course_code = parse_course_code(code)
        except ValueError:
            errors.append(CourseError(course=code, reason="not a valid course code"))
            continue

        try:
            course_sections = fetch_sections(course_code, term, API_KEY)
        except CourseNotFoundError:
            errors.append(CourseError(course=code, reason=f"not found for {term_label}"))
            continue

        if not course_sections:
            errors.append(CourseError(course=code, reason=f"no sections offered for {term_label}"))
            continue

        sections.extend(course_sections)

    if errors:
        raise HTTPException(status_code=400, detail=[error.model_dump() for error in errors])

    return generate_combinations(sections)


# The Docker image copies the built frontend into ./static (see the
# Dockerfile). It doesn't exist in local dev - the Vite dev server handles
# the frontend there instead - so this is skipped unless present.
STATIC_DIR = Path(__file__).parent / "static"
if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
