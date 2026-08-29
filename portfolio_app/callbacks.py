"""Interactions for the project archive and engineering project details."""

from dash import Input, Output, State


def register_callbacks(app):
    """Attach the project archive callbacks."""

    def _register_modal(modal_id, card_id):
        @app.callback(
            Output(modal_id, "opened"),
            Input(card_id, "n_clicks"),
            State(modal_id, "opened"),
            prevent_initial_call=True,
        )
        def toggle_modal(n_clicks, is_open):
            if n_clicks:
                return not is_open
            return is_open

    _register_modal("modal-1", "engineering-card-1")
    _register_modal("modal-2", "engineering-card-2")
    _register_modal("modal-3", "engineering-card-3")
