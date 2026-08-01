# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

watsched generates every valid, conflict-free combination of course sections for a term at the University of Waterloo, so a student can flip through options instead of manually cross-checking lecture/tutorial/test times. Only the backend exists so far; frontend and deployment are not yet built.

## Commands

All commands run from `backend/`.

```bash
# setup
python3 -m venv venv
venv/bin/pip install -r requirements.txt

# run the dev server
venv/bin/uvicorn main:app --port 8000
# then POST to http://127.0.0.1:8000/api/schedules, or use the interactive
# docs at http://127.0.0.1:8000/docs

# tests
venv/bin/pytest                                   # full suite
venv/bin/pytest tests/test_overlap.py::test_shared_day_overlapping_times_is_a_conflict  # single test
```

Requires `backend/.env` with `UWATERLOO_API_KEY=<key>` (get one at openapi.data.uwaterloo.ca/api-docs — register with a `@uwaterloo.ca` email). Never committed; `.env` is git-ignored.

## Architecture

**Data source and its limitation.** All course data comes from UWaterloo's public Open Data API: `GET https://openapi.data.uwaterloo.ca/v3/ClassSchedules/{termCode}/{subject}/{catalogNumber}`, auth via `x-api-key` header. This API does **not** reliably expose which TUT/LAB sections are restricted to which specific LEC section — the field that should carry this (`associatedClassCode`) was confirmed to always be `0`, even on courses where the classes.uwaterloo.ca HTML page shows a real restriction. Because of this, the app does not attempt to model cross-section pairing restrictions at all: the rule is simply "pick exactly one section per (course, component) pair, reject only actual time conflicts."

**Term codes.** UWaterloo term codes are `1` + last 2 digits of year + a term digit (`1`=Winter, `5`=Spring, `9`=Fall), e.g. `1269` = Fall 2026. Implemented in `uwaterloo/term_code.py`, verified against live data.

**Pipeline**, driven by the `POST /api/schedules` endpoint in `main.py`:
1. `uwaterloo/course_code.py: parse_course_code(text)` — free-text course code (e.g. `"cs246"`) → `CourseCode`
2. `uwaterloo/client.py: fetch_sections(course_code, term_code, api_key)` — calls the API, maps raw JSON into `Section` objects. Sections with no scheduled time ("TBA") are silently skipped here.
3. `combinations/generator.py: generate_combinations(sections, limit)` — groups sections into slots by `(course, component)`, then backtracks through picks, pruning via `combinations/overlap.py: sections_overlap` as soon as a partial combination conflicts (not generate-then-filter). Returns a `GenerationResult` with a `truncated` flag if the `limit` was hit.

**Package split:** `uwaterloo/` = everything that knows about UWaterloo's specific API/format. `combinations/` = pure math, zero I/O, would work for any university's data. `schemas.py`/`main.py`/`config.py` stay flat at the root since each is a single distinct role, not a group of similar things.

**`Section` models one meeting time only** (`days`, `start_time`, `end_time`, `start_date`, `end_date` are flat fields on `Section`, not a separate `Meeting` list). This is a deliberate simplification: a section with genuinely different times on different days (rare) will silently only use its first meeting entry from the API.

## Conventions specific to this project

- `schemas.py` holds all Pydantic data-shape models (`Term`, `CourseCode`, `Section`, `Combination`, `GenerationResult`). This project has no database; if one is ever added, DB models belong in a separate `models.py` — `schemas.py` is reserved for API/data shapes only.
- Functions return structured Pydantic models, not tuples or dicts (e.g. `parse_course_code` returns a `CourseCode`, not `(subject, catalog_number)`).
- Every function has a docstring with `Args:`/`Returns:` sections.
- New structure/subpackages get added when a second real consumer needs to reuse a piece, not upfront — this is why `uwaterloo/`/`combinations/` exist now but didn't at first.
- Tests stay flat in `tests/` (not mirrored into `tests/uwaterloo/`, `tests/combinations/`) even though the source is split into packages. Tests use a factory helper (`tests/factories.py: make_section`) instead of constructing full `Section` objects inline, and explicitly cover boundary cases (e.g. one section ending exactly when another starts is *not* a conflict).
- `pytest.ini` sets `pythonpath = .` so tests can import backend modules (`from uwaterloo.client import ...`, `from combinations.overlap import ...`) directly.

## Not yet built

Frontend (planned: calendar view with prev/next through combinations), Dockerfile, and deployment (planned: Google Cloud Run, chosen deliberately over more automated platforms for the ops/Docker learning value).
