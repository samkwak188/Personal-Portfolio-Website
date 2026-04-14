"""Application callbacks."""

from dash import Input, Output, State, ctx

from .cards import (
    build_project_cards,
    build_engineering_cards,
    build_cards_grid,
)
from .data import CODING_PROJECTS, ENGINEERING_PROJECTS


def register_callbacks(app):
    """Attach Dash callbacks to the provided application instance."""

    app.clientside_callback(
        """
        function(tab) {
            if (tab !== "projects") {
                return window.dash_clientside.no_update;
            }
            window.scrollTo({ top: 0, left: 0, behavior: "auto" });
            function resetCoverflow() {
                var el = document.getElementById("projects-coverflow-scroll");
                if (el) {
                    el.scrollLeft = 0;
                }
            }
            resetCoverflow();
            requestAnimationFrame(resetCoverflow);
            setTimeout(resetCoverflow, 0);
            setTimeout(resetCoverflow, 50);
            setTimeout(resetCoverflow, 150);
            return window.dash_clientside.no_update;
        }
        """,
        Output("tab-nav-scroll-store", "data"),
        Input("primary-tabs", "value"),
        prevent_initial_call=True,
    )

    @app.callback(
        Output("primary-tabs", "value"),
        Input("hero-cta-button", "n_clicks"),
        Input("brand-home-button", "n_clicks"),
        State("primary-tabs", "value"),
        prevent_initial_call=True,
    )
    def handle_primary_nav(hero_clicks, home_clicks, current_tab):
        trigger_id = ctx.triggered_id
        if trigger_id == "hero-cta-button" and hero_clicks:
            return "projects"
        if trigger_id == "brand-home-button" and home_clicks:
            return "landing"
        return current_tab

    @app.callback(
        Output("modal-1", "opened"),
        Input("engineering-card-1", "n_clicks"),
        State("modal-1", "opened"),
        prevent_initial_call=True,
    )
    def toggle_modal1(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open

    @app.callback(
        Output("modal-2", "opened"),
        Input("engineering-card-2", "n_clicks"),
        State("modal-2", "opened"),
        prevent_initial_call=True,
    )
    def toggle_modal2(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open

    @app.callback(
        Output("modal-3", "opened"),
        Input("engineering-card-3", "n_clicks"),
        State("modal-3", "opened"),
        prevent_initial_call=True,
    )
    def toggle_modal3(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open

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
