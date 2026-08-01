import pytest

from uwaterloo.course_code import parse_course_code


@pytest.mark.parametrize(
    "text,expected_subject,expected_catalog_number",
    [
        ("cs246", "CS", "246"),
        ("CS 246", "CS", "246"),
        ("math239", "MATH", "239"),
        ("cs136l", "CS", "136L"),
    ],
)
def test_parse_course_code_valid_formats(text, expected_subject, expected_catalog_number):
    result = parse_course_code(text)
    assert result.subject == expected_subject
    assert result.catalog_number == expected_catalog_number


def test_parse_course_code_rejects_garbage_input():
    with pytest.raises(ValueError):
        parse_course_code("not a course code!!")
