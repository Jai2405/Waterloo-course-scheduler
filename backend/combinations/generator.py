from combinations.overlap import sections_overlap
from schemas import Combination, GenerationResult, Section


def group_by_slot(sections: list[Section]) -> list[list[Section]]:
    """Group sections into slots, one slot per (course, component) pair.

    Args:
        sections: All candidate sections across all requested courses.

    Returns:
        List of slots, each slot a list of interchangeable section options.
    """
    slots: dict[tuple[str, str], list[Section]] = {}
    for section in sections:
        key = (section.course, section.component)
        slots.setdefault(key, []).append(section)
    return list(slots.values())


def generate_combinations(sections: list[Section], limit: int = 2000) -> GenerationResult:
    """Generate every valid, conflict-free combination of sections.

    Args:
        sections: All candidate sections across all requested courses.
        limit: Maximum number of combinations to return.

    Returns:
        GenerationResult with the combinations found and whether the limit was hit.
    """
    slots = group_by_slot(sections)
    combinations: list[Combination] = []

    def backtrack(index: int, chosen: list[Section]) -> None:
        if len(combinations) >= limit:
            return
        if index == len(slots):
            combinations.append(Combination(sections=list(chosen)))
            return
        for option in slots[index]:
            if all(not sections_overlap(option, picked) for picked in chosen):
                chosen.append(option)
                backtrack(index + 1, chosen)
                chosen.pop()
                if len(combinations) >= limit:
                    return

    backtrack(0, [])
    return GenerationResult(combinations=combinations, truncated=len(combinations) >= limit)
