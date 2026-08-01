import re

from schemas import CourseCode

COURSE_CODE_PATTERN = re.compile(r"^([a-zA-Z]+)\s*(\d+[a-zA-Z]?)$")


def parse_course_code(text: str) -> CourseCode:
    """Parse a course code like "cs246" into subject and catalog number.

    Args:
        text: Raw course code, e.g. "cs246" or "CS 246".

    Returns:
        CourseCode with subject and catalog_number, e.g. CourseCode(subject="CS", catalog_number="246").
    """
    match = COURSE_CODE_PATTERN.match(text.strip())
    if not match:
        raise ValueError(f"Not a valid course code: {text!r}")

    subject, catalog_number = match.groups()
    return CourseCode(subject=subject.upper(), catalog_number=catalog_number.upper())
