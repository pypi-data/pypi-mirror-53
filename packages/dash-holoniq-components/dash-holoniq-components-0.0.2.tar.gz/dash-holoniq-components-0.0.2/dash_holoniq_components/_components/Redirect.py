# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Redirect(Component):
    """A Redirect component.
Allows the window history/location to be set to a new value

Keyword arguments:
- id (string; required): The ID of this component, used to identify dash components
in callbacks. The ID needs to be unique across all of the
components in an app.
- href (string; optional): href in window.location - e.g., "/my/full/pathname?myargument=1#myhash"
- refresh (boolean; default True): Refresh the page when the location is updated?"""
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, href=Component.UNDEFINED, refresh=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'href', 'refresh']
        self._type = 'Redirect'
        self._namespace = 'dash_holoniq_components/_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'href', 'refresh']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Redirect, self).__init__(**args)
