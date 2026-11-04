import pyray as rl
from collections.abc import Callable

from openpilot.selfdrive.controls.lib.lead_gap_offset import get_lead_gap_options, read_lead_gap_offset, write_lead_gap_offset
from openpilot.selfdrive.ui.mici.layouts.settings.initial_cruise_speed import SpeedScroller, CENTER_FONT_SIZE, CENTER_LETTER_SPACING, \
                                                                           SIDE_FONT_SIZE, SIDE_LETTER_SPACING, ITEM_DRAG_DISTANCE
from openpilot.selfdrive.ui.mici.widgets.button import BigButton, LABEL_COLOR
from openpilot.selfdrive.ui.mici.widgets.dialog import BigDialogBase
from openpilot.system.ui.lib.application import gui_app, FontWeight, TextAlignment, FONT_SCALE
from openpilot.system.ui.lib.text_measure import measure_text_cached
from openpilot.system.ui.widgets import Widget
from openpilot.system.ui.widgets.label import UnifiedLabel


def _format(value: float) -> str:
  return f"{value:.1f}"


def _current_index(values: list[float]) -> int:
  current = read_lead_gap_offset()
  return min(range(len(values)), key=lambda i: abs(values[i] - current))


class LeadGapScroller(SpeedScroller):
  def show_event(self):
    Widget.show_event(self)
    self._values = get_lead_gap_options()
    self._options = [_format(v) for v in self._values]
    self._locked_idx = _current_index(self._values)
    self._center_widths = [measure_text_cached(self._center_font, option, CENTER_FONT_SIZE,
                                               CENTER_LETTER_SPACING * CENTER_FONT_SIZE * FONT_SCALE).x for option in self._options]
    self._side_widths = [measure_text_cached(self._side_font, option, SIDE_FONT_SIZE,
                                             SIDE_LETTER_SPACING * SIDE_FONT_SIZE * FONT_SCALE).x for option in self._options]

    self._scroll_panel.set_offset(-self._locked_idx * ITEM_DRAG_DISTANCE)

  def _lock(self, idx: int):
    self._locked_idx = self._clamp_index(idx)
    write_lead_gap_offset(self._values[self._locked_idx])
    self._change_callback()


class LeadGapPicker(BigDialogBase):
  def __init__(self, change_callback: Callable[[], None]):
    super().__init__()
    self._unit_label = self._child(UnifiedLabel("extra meters", 36, FontWeight.BOLD, LABEL_COLOR, alignment=TextAlignment.CENTER,
                                                letter_spacing=-0.03))
    self._scroller = self._child(LeadGapScroller(change_callback))
    self._scroller.set_enabled(lambda: self.enabled and not self.is_dismissing)

  def _render(self, _):
    self._scroller.render(self._rect)
    self._unit_label.render(rl.Rectangle(self._rect.x, self._rect.y + 166, self._rect.width, self._rect.height - 166))


class LeadGapButton(BigButton):
  def __init__(self):
    super().__init__("lead car gap", " ", description="Extra space kept behind the lead car, in meters.\n" +
                                                      "Applies when stopped and while following.\n" +
                                                      "Takes effect on the next drive.")
    self._picker = LeadGapPicker(self.refresh)
    self.set_click_callback(lambda: gui_app.push_widget(self._picker))
    self.refresh()

  def _get_label_font_size(self):
    return 42

  def refresh(self):
    self.set_value(f"+{_format(read_lead_gap_offset())} m")
