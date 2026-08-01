from schemas import Term
from uwaterloo.term_code import term_code


def test_term_code_fall():
    assert term_code(Term(year=2026, term="fall")) == "1269"


def test_term_code_winter():
    assert term_code(Term(year=2026, term="winter")) == "1261"


def test_term_code_spring():
    assert term_code(Term(year=2026, term="spring")) == "1265"
