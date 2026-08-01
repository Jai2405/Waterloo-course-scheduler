from schemas import Term

TERM_DIGITS = {"winter": "1", "spring": "5", "fall": "9"}


def term_code(term: Term) -> str:
    """Convert a Term into UWaterloo's term code.

    Args:
        term: Year and term name (winter/spring/fall).

    Returns:
        UWaterloo term code, e.g. "1269" for Term(year=2026, term="fall").
    """
    return f"1{term.year % 100:02d}{TERM_DIGITS[term.term]}"
