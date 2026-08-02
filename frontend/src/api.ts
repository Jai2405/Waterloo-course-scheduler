import type { CourseError, GenerationResult, ScheduleRequest } from "./types"

export type ScheduleOutcome =
  | { kind: "success"; data: GenerationResult }
  | { kind: "courseErrors"; errors: CourseError[] }
  | { kind: "unknownError"; message: string }

export async function generateSchedules(request: ScheduleRequest): Promise<ScheduleOutcome> {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/schedules", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    })

    if (response.ok) {
      const data: GenerationResult = await response.json()
      return { kind: "success", data }
    }

    if (response.status === 400) {
      const body = await response.json()
      return { kind: "courseErrors", errors: body.detail as CourseError[] }
    }

    return { kind: "unknownError", message: `Server error (${response.status})` }
  } catch {
    return { kind: "unknownError", message: "Couldn't reach the server" }
  }
}
