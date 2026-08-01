from combinations.generator import generate_combinations, group_by_slot
from tests.factories import make_section


def test_group_by_slot_groups_by_course_and_component():
    lec1 = make_section(course="CS246", component="LEC", section_number=1)
    lec2 = make_section(course="CS246", component="LEC", section_number=2)
    tut1 = make_section(course="CS246", component="TUT", section_number=101)

    slots = group_by_slot([lec1, lec2, tut1])

    assert len(slots) == 2  # one LEC slot, one TUT slot
    assert sorted(len(slot) for slot in slots) == [1, 2]


def test_generate_combinations_returns_full_cartesian_product_when_nothing_conflicts():
    lec1 = make_section(course="CS246", component="LEC", section_number=1, days=["M"])
    lec2 = make_section(course="CS246", component="LEC", section_number=2, days=["M"])
    tut1 = make_section(course="CS246", component="TUT", section_number=101, days=["T"])

    result = generate_combinations([lec1, lec2, tut1])

    assert len(result.combinations) == 2  # 2 LEC options x 1 TUT option
    assert result.truncated is False


def test_generate_combinations_excludes_conflicting_pairs():
    lec = make_section(course="CS246", component="LEC", section_number=1, days=["M"], start="09:00", end="10:00")
    tut_conflict = make_section(
        course="CS246", component="TUT", section_number=101, days=["M"], start="09:30", end="10:30"
    )
    tut_ok = make_section(course="CS246", component="TUT", section_number=102, days=["T"], start="09:00", end="10:00")

    result = generate_combinations([lec, tut_conflict, tut_ok])

    assert len(result.combinations) == 1
    assert result.combinations[0].sections[1].section_number == 102


def test_generate_combinations_returns_empty_when_every_combination_conflicts():
    lec = make_section(course="CS246", component="LEC", section_number=1, days=["M"], start="09:00", end="10:00")
    tut = make_section(course="CS246", component="TUT", section_number=101, days=["M"], start="09:00", end="10:00")

    result = generate_combinations([lec, tut])

    assert result.combinations == []
    assert result.truncated is False


def test_generate_combinations_stops_at_limit_and_flags_truncated():
    lecs = [make_section(course="CS246", component="LEC", section_number=i) for i in range(5)]

    result = generate_combinations(lecs, limit=2)

    assert len(result.combinations) == 2
    assert result.truncated is True
