from schemas import Section


def sections_overlap(a: Section, b: Section) -> bool:
    """Check whether two sections conflict in time.

    Args:
        a: First section.
        b: Second section.

    Returns:
        True if they share a weekday and their times overlap on that day.
    """
    shared_days = set(a.days) & set(b.days)
    if not shared_days:
        return False

    return a.start_time < b.end_time and b.start_time < a.end_time
