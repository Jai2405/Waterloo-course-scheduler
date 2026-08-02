export type Term = {
  year: number
  term: "winter" | "spring" | "fall"
}

export type ScheduleRequest = {
  term: Term
  courses: string[]
}

export type Section = {
  course: string
  component: string
  section_number: number
  class_number: number
  days: string[]
  start_time: string
  end_time: string
  start_date: string
  end_date: string
}

export type Combination = {
  sections: Section[]
}

export type GenerationResult = {
  combinations: Combination[]
  truncated: boolean
}

export type CourseError = {
  course: string
  reason: string
}
