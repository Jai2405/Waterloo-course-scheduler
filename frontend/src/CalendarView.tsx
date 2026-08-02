import {
  DAY_LABELS,
  DAY_ORDER,
  END_HOUR,
  START_HOUR,
  TIME_SLOT_COUNT,
  formatTime,
  rowForTime,
} from "./calendar"
import type { Combination } from "./types"

type CalendarViewProps = {
  combination: Combination
}

function CalendarView({ combination }: CalendarViewProps) {
  const hours = Array.from({ length: END_HOUR - START_HOUR }, (_, i) => START_HOUR + i)

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: `60px repeat(${DAY_ORDER.length}, 1fr)`,
        gridTemplateRows: `auto repeat(${TIME_SLOT_COUNT}, 4px)`,
        border: "1px solid #ccc",
      }}
    >
      {DAY_ORDER.map((day, i) => (
        <div key={day} style={{ gridColumn: i + 2, gridRow: 1, fontWeight: "bold", textAlign: "center" }}>
          {DAY_LABELS[day]}
        </div>
      ))}

      {hours.map((hour) => (
        <div
          key={hour}
          style={{ gridColumn: 1, gridRow: rowForTime(`${hour}:00:00`), fontSize: "0.7rem", color: "#666" }}
        >
          {hour}:00
        </div>
      ))}

      {combination.sections.flatMap((section) =>
        section.days
          .filter((day) => DAY_ORDER.includes(day as (typeof DAY_ORDER)[number]))
          .map((day) => (
            <div
              key={`${section.course}-${section.component}-${section.section_number}-${day}`}
              style={{
                gridColumn: DAY_ORDER.indexOf(day as (typeof DAY_ORDER)[number]) + 2,
                gridRow: `${rowForTime(section.start_time)} / ${rowForTime(section.end_time)}`,
                background: "#eee",
                border: "1px solid #999",
                fontSize: "0.7rem",
                padding: "2px",
                overflow: "hidden",
              }}
            >
              {section.course} {section.component}
              <br />
              {formatTime(section.start_time)}
            </div>
          )),
      )}
    </div>
  )
}

export default CalendarView
