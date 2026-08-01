from datetime import date, time

from schemas import Section


def make_section(
    course: str = "TEST101",
    component: str = "LEC",
    section_number: int = 1,
    days: list[str] | None = None,
    start: str = "10:00",
    end: str = "11:00",
) -> Section:
    """Build a Section for tests without repeating every field each time.

    Args:
        course: Course code, e.g. "CS246".
        component: Section type, e.g. "LEC".
        section_number: Section number.
        days: Weekdays, e.g. ["T", "R"]. Defaults to ["M"].
        start: Start time as "HH:MM".
        end: End time as "HH:MM".

    Returns:
        A Section with the given values and fixed dummy dates/class number.
    """
    return Section(
        course=course,
        component=component,
        section_number=section_number,
        class_number=1000 + section_number,
        days=days or ["M"],
        start_time=time.fromisoformat(start),
        end_time=time.fromisoformat(end),
        start_date=date(2026, 9, 9),
        end_date=date(2026, 12, 8),
    )
