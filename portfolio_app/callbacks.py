"""Interactions for the project archive and engineering project details."""

from dash import Input, Output, State

from .cards import build_cards_grid, build_engineering_cards, build_project_cards
from .data import CODING_PROJECTS, ENGINEERING_PROJECTS


def register_callbacks(app):
    """Attach the project archive callbacks."""

    @app.callback(
        Output("projects-grid", "children"),
        Input("project-category-toggle", "value"),
        prevent_initial_call=False,
    )
    def switch_project_category(category):
        if category == "engineering":
            cards = build_engineering_cards(ENGINEERING_PROJECTS)
        else:
            cards = build_project_cards(CODING_PROJECTS)
        return build_cards_grid(cards)

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
