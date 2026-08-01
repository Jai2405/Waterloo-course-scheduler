from datetime import date, time
from typing import Literal

from pydantic import BaseModel


class Term(BaseModel):
    """A term selection, e.g. year=2026, term="fall"."""

    year: int
    term: Literal["winter", "spring", "fall"]


class CourseCode(BaseModel):
    """A course code split into its parts, e.g. "cs246" -> subject="CS", catalog_number="246"."""

    subject: str
    catalog_number: str


class Section(BaseModel):
    """One enrollable section (e.g. "CS246 LEC 001") with its single weekly meeting time."""

    course: str
    component: str
    section_number: int
    class_number: int
    days: list[str]
    start_time: time
    end_time: time
    start_date: date
    end_date: date


class ScheduleRequest(BaseModel):
    """A request to generate all valid schedule combinations for a term."""

    term: Term
    courses: list[str]


class Combination(BaseModel):
    """One valid, conflict-free pick of sections, one per course+component slot."""

    sections: list[Section]


class GenerationResult(BaseModel):
    """Output of generating all valid combinations."""

    combinations: list[Combination]
    truncated: bool
