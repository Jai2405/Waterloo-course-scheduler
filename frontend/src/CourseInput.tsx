import { useState } from "react"

type CourseInputProps = {
  courses: string[]
  onChange: (courses: string[]) => void
}

function CourseInput({ courses, onChange }: CourseInputProps) {
  const [text, setText] = useState("")

  function addCourse() {
    const trimmed = text.trim()
    const alreadyAdded = courses.some((c) => c.toLowerCase() === trimmed.toLowerCase())
    if (trimmed && !alreadyAdded) {
      onChange([...courses, trimmed])
      setText("")
    }
  }

  function removeCourse(index: number) {
    onChange(courses.filter((_, i) => i !== index))
  }

  return (
    <div>
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            e.preventDefault()
            addCourse()
          }
        }}
        placeholder="e.g. cs246"
      />
      <button type="button" onClick={addCourse}>
        Add
      </button>
      <ul>
        {courses.map((course, index) => (
          <li key={course}>
            {course}
            <button type="button" onClick={() => removeCourse(index)}>
              ×
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default CourseInput
