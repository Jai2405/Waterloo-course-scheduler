from combinations.overlap import sections_overlap
from tests.factories import make_section


def test_no_shared_days_is_not_a_conflict():
    a = make_section(days=["M"], start="10:00", end="11:00")
    b = make_section(days=["T"], start="10:00", end="11:00")
    assert sections_overlap(a, b) is False


def test_shared_day_overlapping_times_is_a_conflict():
    a = make_section(days=["T"], start="10:00", end="11:00")
    b = make_section(days=["T"], start="10:30", end="11:30")
    assert sections_overlap(a, b) is True


def test_shared_day_non_overlapping_times_is_not_a_conflict():
    a = make_section(days=["T"], start="10:00", end="11:00")
    b = make_section(days=["T"], start="11:30", end="12:30")
    assert sections_overlap(a, b) is False


def test_back_to_back_times_touching_at_the_boundary_is_not_a_conflict():
    a = make_section(days=["T"], start="10:00", end="11:00")
    b = make_section(days=["T"], start="11:00", end="12:00")
    assert sections_overlap(a, b) is False


def test_only_one_shared_day_overlapping_is_still_a_conflict():
    a = make_section(days=["M", "W"], start="10:00", end="11:00")
    b = make_section(days=["W", "F"], start="10:30", end="11:30")
    assert sections_overlap(a, b) is True
