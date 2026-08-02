import { getUpcomingTerms, termLabel } from "./term"
import type { Term } from "./types"

const UPCOMING_TERMS = getUpcomingTerms(3)

type TermSelectProps = {
  value: Term
  onChange: (term: Term) => void
}

function TermSelect({ value, onChange }: TermSelectProps) {
  return (
    <select
      value={termLabel(value)}
      onChange={(e) => {
        const selected = UPCOMING_TERMS.find((t) => termLabel(t) === e.target.value)
        if (selected) onChange(selected)
      }}
    >
      {UPCOMING_TERMS.map((term) => (
        <option key={termLabel(term)} value={termLabel(term)}>
          {termLabel(term)}
        </option>
      ))}
    </select>
  )
}

export default TermSelect
