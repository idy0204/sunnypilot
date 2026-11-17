import os

# On/off for the +10 mph offset on 55 mph+ limits. Plain file because the params key list is compiled into libparams_c.so.
SPEED_LIMIT_TIER_FILE = "/data/gv70/speed_limit_tier"


def read_speed_limit_tier() -> bool:
  try:
    with open(SPEED_LIMIT_TIER_FILE) as f:
      return f.read().strip() != "0"
  except OSError:
    return True  # missing file = on


def write_speed_limit_tier(enabled: bool) -> None:
  os.makedirs(os.path.dirname(SPEED_LIMIT_TIER_FILE), exist_ok=True)
  tmp = SPEED_LIMIT_TIER_FILE + ".tmp"
  with open(tmp, "w") as f:
    f.write("1" if enabled else "0")
    f.flush()
    os.fsync(f.fileno())
  os.replace(tmp, SPEED_LIMIT_TIER_FILE)
