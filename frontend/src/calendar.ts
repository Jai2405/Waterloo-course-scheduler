export const START_HOUR = 8
export const END_HOUR = 22

const ROW_MINUTES = 10
const FIRST_TIME_ROW = 2

export const TIME_SLOT_COUNT = ((END_HOUR - START_HOUR) * 60) / ROW_MINUTES

export const DAY_ORDER = ["M", "T", "W", "R", "F"] as const
export const DAY_LABELS: Record<string, string> = {
  M: "Mon",
  T: "Tue",
  W: "Wed",
  R: "Thu",
  F: "Fri",
}

function timeToMinutes(time: string): number {
  const [hours, minutes] = time.split(":").map(Number)
  return hours * 60 + minutes
}

/** Grid row for a given time. Row 1 is the day-label header; time rows start at row 2. */
export function rowForTime(time: string): number {
  const minutesFromStart = timeToMinutes(time) - START_HOUR * 60
  return minutesFromStart / ROW_MINUTES + FIRST_TIME_ROW
}

export function formatTime(time: string): string {
  const [hoursStr, minutesStr] = time.split(":")
  const hours = Number(hoursStr)
  const period = hours >= 12 ? "PM" : "AM"
  const displayHours = hours % 12 === 0 ? 12 : hours % 12
  return `${displayHours}:${minutesStr} ${period}`
}
