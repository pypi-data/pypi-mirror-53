from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .VuetifyWidget import VuetifyWidget


class Input(VuetifyWidget):

    _model_name = Unicode('InputModel').tag(sync=True)

    append_icon = Unicode(None, allow_none=True).tag(sync=True)

    background_color = Unicode(None, allow_none=True).tag(sync=True)

    color = Unicode(None, allow_none=True).tag(sync=True)

    dark = Bool(None, allow_none=True).tag(sync=True)

    disabled = Bool(None, allow_none=True).tag(sync=True)

    error = Bool(None, allow_none=True).tag(sync=True)

    error_count = Union([
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)

    error_messages = Union([
        Unicode(),
        List(Any())
    ], default_value=None, allow_none=True).tag(sync=True)

    height = Union([
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)

    hide_details = Bool(None, allow_none=True).tag(sync=True)

    hint = Unicode(None, allow_none=True).tag(sync=True)

    id = Unicode(None, allow_none=True).tag(sync=True)

    label = Unicode(None, allow_none=True).tag(sync=True)

    light = Bool(None, allow_none=True).tag(sync=True)

    loading = Bool(None, allow_none=True).tag(sync=True)

    messages = Union([
        Unicode(),
        List(Any())
    ], default_value=None, allow_none=True).tag(sync=True)

    persistent_hint = Bool(None, allow_none=True).tag(sync=True)

    prepend_icon = Unicode(None, allow_none=True).tag(sync=True)

    readonly = Bool(None, allow_none=True).tag(sync=True)

    rules = List(Any(), default_value=None, allow_none=True).tag(sync=True)

    success = Bool(None, allow_none=True).tag(sync=True)

    success_messages = Union([
        Unicode(),
        List(Any())
    ], default_value=None, allow_none=True).tag(sync=True)

    validate_on_blur = Bool(None, allow_none=True).tag(sync=True)

    value = Any(None, allow_none=True).tag(sync=True)


__all__ = ['Input']
