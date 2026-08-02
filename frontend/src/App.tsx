import { useState } from "react"
import { generateSchedules } from "./api"
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
  const [courseErrors, setCourseErrors] = useState<CourseError[] | null>(null)
  const [generalError, setGeneralError] = useState<string | null>(null)

  async function handleGenerate() {
    setLoading(true)
    setResult(null)
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
      <TermSelect value={term} onChange={setTerm} />
      <CourseInput courses={courses} onChange={setCourses} />
      <button type="button" onClick={handleGenerate} disabled={loading || courses.length < MIN_COURSES}>
        {loading ? "Generating..." : "Generate"}
      </button>

      {courses.length < MIN_COURSES && <p>Add at least {MIN_COURSES} courses to generate schedules.</p>}

      {courseErrors && (
        <ul>
          {courseErrors.map((e) => (
            <li key={e.course}>
              {e.course}: {e.reason}
            </li>
          ))}
        </ul>
      )}

      {generalError && <p>{generalError}</p>}

      {result && <p>{result.combinations.length} combinations found.</p>}
    </div>
  )
}

export default App
