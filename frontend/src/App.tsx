import { useState } from "react"
import { generateSchedules } from "./api"
import CalendarView from "./CalendarView"
import CourseInput from "./CourseInput"
import TermSelect from "./TermSelect"
import { getUpcomingTerms } from "./term"
import type { CourseError, GenerationResult, Term } from "./types"

const MIN_COURSES = 3

function App() {
  const [term, setTerm] = useState<Term>(getUpcomingTerms(1)[0])
  const [courses, setCourses] = useState<string[]>([])
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<GenerationResult | null>(null)
  const [viewIndex, setViewIndex] = useState(0)
  const [courseErrors, setCourseErrors] = useState<CourseError[] | null>(null)
  const [generalError, setGeneralError] = useState<string | null>(null)

  async function handleGenerate() {
    setLoading(true)
    setResult(null)
    setViewIndex(0)
    setCourseErrors(null)
    setGeneralError(null)

    const outcome = await generateSchedules({ term, courses })

    if (outcome.kind === "success") {
      setResult(outcome.data)
    } else if (outcome.kind === "courseErrors") {
      setCourseErrors(outcome.errors)
    } else {
      setGeneralError(outcome.message)
    }

    setLoading(false)
  }

  return (
    <div>
      <h1>watsched</h1>

      <div className="field">
        <TermSelect value={term} onChange={setTerm} />
      </div>

      <div className="field">
        <CourseInput courses={courses} onChange={setCourses} />
      </div>

      <button type="button" onClick={handleGenerate} disabled={loading || courses.length < MIN_COURSES}>
        {loading ? "Generating..." : "Generate"}
      </button>

      {courses.length < MIN_COURSES && (
        <p className="hint">Add at least {MIN_COURSES} courses to generate schedules.</p>
      )}

      {courseErrors && (
        <ul className="error-list">
          {courseErrors.map((e) => (
            <li key={e.course}>
              {e.course}: {e.reason}
            </li>
          ))}
        </ul>
      )}

      {generalError && <p className="error-message">{generalError}</p>}

      {result && result.combinations.length === 0 && (
        <p className="error-message">No valid combinations found - every option conflicts.</p>
      )}

      {result && result.combinations.length > 0 && (
        <div>
          <div className="nav">
            <button type="button" onClick={() => setViewIndex((i) => i - 1)} disabled={viewIndex === 0}>
              Prev
            </button>
            <span>
              {viewIndex + 1} / {result.combinations.length}
            </span>
            <button
              type="button"
              onClick={() => setViewIndex((i) => i + 1)}
              disabled={viewIndex === result.combinations.length - 1}
            >
              Next
            </button>
          </div>
          <div className="calendar">
            <CalendarView combination={result.combinations[viewIndex]} />
          </div>
        </div>
      )}
    </div>
  )
}

export default App
