from datetime import date, time

import httpx

from schemas import CourseCode, Section


class CourseNotFoundError(Exception):
    """Raised when UWaterloo has no record of a course (bad subject/catalog number)."""


def fetch_sections(course_code: CourseCode, term_code: str, api_key: str) -> list[Section]:
    """Fetch and parse all sections for one course in one term from UWaterloo's API.

    Args:
        course_code: Parsed subject + catalog number.
        term_code: UWaterloo term code, e.g. "1269".
        api_key: UWaterloo Open Data API key.

    Returns:
        List of Section, one per section (LEC/TUT/TST/...) UWaterloo returns.
        Empty list if the course exists but has no sections offered this term.

    Raises:
        CourseNotFoundError: If UWaterloo has no record of this course at all.
    """
    url = (
        f"https://openapi.data.uwaterloo.ca/v3/ClassSchedules/"
        f"{term_code}/{course_code.subject}/{course_code.catalog_number}"
    )
    response = httpx.get(url, headers={"x-api-key": api_key}, timeout=5)
    if response.status_code == 404:
        raise CourseNotFoundError(f"{course_code.subject}{course_code.catalog_number} not found")
    response.raise_for_status()

    sections = []
    for raw in response.json():
        # A section can technically have more than one distinct meeting time
        # (rare). We're keeping this simple and only using the first one.
        if not raw["scheduleData"]:
            continue
        meeting = raw["scheduleData"][0]

        # Time TBA sections have no scheduled time yet - skip them.
        if meeting["classMeetingStartTime"] is None or meeting["classMeetingEndTime"] is None:
            continue

        sections.append(
            Section(
                course=f"{course_code.subject}{course_code.catalog_number}",
                component=raw["courseComponent"],
                section_number=raw["classSection"],
                class_number=raw["classNumber"],
                days=list(meeting["classMeetingDayPatternCode"]),
                start_time=time.fromisoformat(meeting["classMeetingStartTime"][11:]),
                end_time=time.fromisoformat(meeting["classMeetingEndTime"][11:]),
                start_date=date.fromisoformat(meeting["scheduleStartDate"][:10]),
                end_date=date.fromisoformat(meeting["scheduleEndDate"][:10]),
            )
        )
    return sections
