import os

# Extra gap kept to the vision lead, in meters. Stored in a plain file because the params key list is compiled into libparams_c.so.
LEAD_GAP_OFFSET_FILE = "/data/gv70/lead_gap_offset"
LEAD_GAP_OFFSET_DEFAULT = 1.0
LEAD_GAP_OFFSET_MIN = 0.0
LEAD_GAP_OFFSET_MAX = 2.0
LEAD_GAP_OFFSET_STEP = 0.1


def get_lead_gap_options() -> list[float]:
  steps = round((LEAD_GAP_OFFSET_MAX - LEAD_GAP_OFFSET_MIN) / LEAD_GAP_OFFSET_STEP)
  return [round(LEAD_GAP_OFFSET_MIN + i * LEAD_GAP_OFFSET_STEP, 1) for i in range(steps + 1)]


def read_lead_gap_offset() -> float:
  try:
    with open(LEAD_GAP_OFFSET_FILE) as f:
      value = float(f.read().strip())
  except (OSError, ValueError):
    return LEAD_GAP_OFFSET_DEFAULT
  if value != value:  # NaN
    return LEAD_GAP_OFFSET_DEFAULT
  return round(min(max(value, LEAD_GAP_OFFSET_MIN), LEAD_GAP_OFFSET_MAX), 1)


def write_lead_gap_offset(value: float) -> None:
  value = round(min(max(value, LEAD_GAP_OFFSET_MIN), LEAD_GAP_OFFSET_MAX), 1)
  os.makedirs(os.path.dirname(LEAD_GAP_OFFSET_FILE), exist_ok=True)
  tmp = LEAD_GAP_OFFSET_FILE + ".tmp"
  with open(tmp, "w") as f:
    f.write(f"{value:.1f}")
    f.flush()
    os.fsync(f.fileno())
  os.replace(tmp, LEAD_GAP_OFFSET_FILE)
