from .labels import Labels
from ._constants import Mode


@Labels.bind_key('Space')
def hold_to_pan_zoom(layer):
    if layer._mode != Mode.PAN_ZOOM:
        # on key press
        prev_mode = layer.mode
        layer.mode = Mode.PAN_ZOOM

        yield

        # on key release
        layer.mode = prev_mode


@Labels.bind_key('P')
def activate_paint_mode(layer):
    layer.mode = Mode.PAINT


@Labels.bind_key('F')
def activate_fill_mode(layer):
    layer.mode = Mode.FILL


@Labels.bind_key('Z')
def activate_pan_zoom_mode(layer):
    layer.mode = Mode.PAN_ZOOM


@Labels.bind_key('L')
def activate_picker_mode(layer):
    layer.mode = Mode.PICKER


@Labels.bind_key('E')
def erase(layer):
    layer.selected_label = 0


@Labels.bind_key('M')
def new_label(layer):
    layer.selected_label = layer.data.max() + 1


@Labels.bind_key('D')
def decrease_label_id(layer):
    layer.selected_label -= 1


@Labels.bind_key('I')
def increase_label_id(layer):
    layer.selected_label += 1


Labels.bind_key('Control-Z', Labels.undo)
Labels.bind_key('Control-Shift-Z', Labels.redo)
