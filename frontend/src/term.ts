import type { Term } from "./types"

const TERM_ORDER: Term["term"][] = ["winter", "spring", "fall"]

function currentTermIndex(now: Date): number {
  const month = now.getMonth() // 0-11
  if (month <= 3) return 0 // winter: Jan-Apr
  if (month <= 7) return 1 // spring: May-Aug
  return 2 // fall: Sep-Dec
}

export function getUpcomingTerms(count: number, now: Date = new Date()): Term[] {
  const terms: Term[] = []
  let index = currentTermIndex(now)
  let year = now.getFullYear()

  for (let i = 0; i < count; i++) {
    index = (index + 1) % 3
    if (index === 0) year += 1
    terms.push({ year, term: TERM_ORDER[index] })
  }

  return terms
}

export function termLabel(term: Term): string {
  const capitalized = term.term.charAt(0).toUpperCase() + term.term.slice(1)
  return `${capitalized} ${term.year}`
}
