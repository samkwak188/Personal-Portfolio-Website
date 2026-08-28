"""Reusable cards for the horizontal project archive."""

from typing import Iterable, List

import dash_mantine_components as dmc
from dash import html


_IMAGE_STYLE = {
    "height": "220px",
    "objectFit": "cover",
    "width": "100%",
}


def _project_links(project):
    links = []
    for label, key in (("Demo", "demo_url"), ("Live site", "live_url"), ("GitHub", "github_url")):
        url = project.get(key)
        if not url:
            continue
        links.append(
            html.A(
                f"{label} ↗",
                href=url,
                target="_blank",
                rel="noopener noreferrer",
                className="project-card-link",
            )
        )
    return links


def create_project_card(project: dict) -> dmc.Card:
    """Return a software project card."""
    return dmc.Card(
        [
            dmc.CardSection(
                dmc.Image(
                    src=project["image_src"],
                    alt=project["image_alt"],
                    style=_IMAGE_STYLE,
                )
            ),
            html.Div(
                [
                    html.H3(project["title"], className="project-card-title"),
                    html.P(project["description"], className="project-card-description"),
                    html.Div(_project_links(project), className="project-card-links"),
                ],
                className="project-card-body",
            ),
        ],
        className="project-card",
        withBorder=False,
        padding=0,
    )


def create_engineering_card(project: dict) -> html.Div:
    """Return a hardware project card that opens its detail modal."""
    card = dmc.Card(
        [
            dmc.CardSection(
                dmc.Image(
                    src=project["image_src"],
                    alt=project["image_alt"],
                    style=_IMAGE_STYLE,
                )
            ),
            html.Div(
                [
                    html.H3(project["title"], className="project-card-title"),
                    html.P(project["description"], className="project-card-description"),
                    html.Span("Open details ↗", className="project-card-link"),
                ],
                className="project-card-body",
            ),
        ],
        className="project-card engineering-project-card",
        withBorder=False,
        padding=0,
    )
    return html.Div(card, id=project["id"], n_clicks=0, className="engineering-card-trigger")


def build_project_cards(projects: Iterable[dict]) -> List[html.Div]:
    return [html.Div(create_project_card(project)) for project in list(projects)]


def build_engineering_cards(projects: Iterable[dict]) -> List[html.Div]:
    return [create_engineering_card(project) for project in list(projects)]


def build_cards_grid(card_children: Iterable[html.Div]) -> html.Div:
    """Preserve the original scroll-snap coverflow interaction."""
    items = [
        html.Div(
            html.Div(
                [card, html.Div(className="coverflow-shadow")],
                className="coverflow-surface",
            ),
            className="coverflow-item",
            **{"data-coverflow-item": "true"},
        )
        for card in list(card_children)
    ]
    return html.Div(
        [
            html.Div(
                items,
                id="projects-coverflow-scroll",
                className="coverflow-scroll",
                **{"aria-label": "Scrollable project archive"},
            ),
            html.P("Scroll or swipe to browse every project", className="coverflow-hint"),
        ],
        className="coverflow-root",
    )
