"""Reusable card component builders."""

from typing import Iterable, List

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from .theme import CARD_STYLE

_CARD_IMAGE_STYLE = {
    "height": "240px",
    "objectFit": "cover",
    "width": "100%",
    "borderTopLeftRadius": "14px",
    "borderTopRightRadius": "14px",
}
_CARD_IMAGE_SECTION_STYLE = {"flex": "0 0 auto", "padding": "0"}
_CARD_BODY_TEXT_STYLE = {
    "flexGrow": 1,
    "lineHeight": "1.6",
    "color": "#cbd5e1",
}
_BUTTON_CONTAINER_STYLE = {"marginTop": "auto", "paddingTop": "16px"}
_BUTTON_PROPS = {
    "size": "xs",
    "variant": "outline",
    "radius": "xl",
    "className": "project-btn",
    "style": {
        "borderColor": "rgba(255,255,255,0.2)",
        "color": "#e2e8f0",
        "transition": "all 0.2s",
    },
}
_BUTTON_ICONS = {
    "Demo Video": {"icon": "logos:youtube-icon", "width": 16},
    "Live Demo": {"icon": "heroicons:rocket-launch-solid", "width": 16},
    "GitHub": {"icon": "ion:logo-github", "width": 16},
}
_BUTTON_CONFIG = (
    ("Demo Video", "demo_url"),
    ("Live Demo", "live_url"),
    ("GitHub", "github_url"),
)
_GRID_STYLE = {
    "gridTemplateColumns": "repeat(auto-fit, minmax(320px, 1fr))",
    "display": "grid",
    "gap": "32px",
    "alignItems": "stretch",
}


def create_project_card(project: dict) -> dmc.Card:
    """Return a project card component for the given project definition."""
    buttons = []
    for label, url_key in _BUTTON_CONFIG:
        url = project.get(url_key)
        if not url:
            continue
        icon_cfg = _BUTTON_ICONS.get(label)
        left_section = (
            DashIconify(icon=icon_cfg["icon"], width=icon_cfg["width"])
            if icon_cfg
            else None
        )

        buttons.append(
            html.A(
                dmc.Button(
                    label,
                    leftSection=left_section,
                    **_BUTTON_PROPS,
                ),
                href=url,
                target="_blank",
                rel="noopener noreferrer",
                style={"textDecoration": "none"},
            )
        )

    accent = project.get("accent", "#1a1a2e")

    card_style = {
        "width": "100%",
        "height": "100%",
        "display": "flex",
        "flexDirection": "column",
        "background": f"linear-gradient(180deg, {accent} 0%, {accent} 40%, {accent} 100%)",
        "border": "1px solid rgba(255,255,255,0.08)",
        "borderRadius": "14px",
        "overflow": "hidden",
    }

    return dmc.Card(
        children=[
            dmc.CardSection(
                dmc.Image(
                    src=project["image_src"],
                    alt=project["image_alt"],
                    style=_CARD_IMAGE_STYLE,
                ),
                style=_CARD_IMAGE_SECTION_STYLE,
            ),
            dmc.Stack(
                [
                    dmc.Text(
                        project["title"],
                        fw=700,
                        size="md",
                        c="white",
                        style={"letterSpacing": "-0.3px"}
                    ),
                    dmc.Text(
                        project["description"],
                        size="xs",
                        style=_CARD_BODY_TEXT_STYLE,
                        lineClamp=3,
                    ),
                    dmc.Box(
                        dmc.Group(buttons, gap="xs", wrap="wrap") if buttons else None,
                        style=_BUTTON_CONTAINER_STYLE,
                    ),
                ],
                p="md",
                style={"flex": 1, "display": "flex", "flexDirection": "column"},
            ),
        ],
        withBorder=False,
        shadow="md",
        radius="lg",
        style=card_style,
        className="card-hover",
    )


def create_engineering_card(project: dict) -> html.Div:
    """Return an engineering project card wrapper with the expected ID."""
    accent = project.get("accent", "#1a1a2e")

    card_style = {
        "width": "100%",
        "height": "100%",
        "display": "flex",
        "flexDirection": "column",
        "background": f"linear-gradient(180deg, {accent} 0%, {accent} 40%, {accent} 100%)",
        "border": "1px solid rgba(255,255,255,0.08)",
        "borderRadius": "14px",
        "overflow": "hidden",
        "cursor": "pointer",
    }

    card = dmc.Card(
        children=[
            dmc.CardSection(
                dmc.Image(
                    src=project["image_src"],
                    alt=project["image_alt"],
                    style=_CARD_IMAGE_STYLE,
                ),
                style=_CARD_IMAGE_SECTION_STYLE,
            ),
            dmc.Stack(
                [
                    dmc.Text(
                        project["title"],
                        fw=700,
                        size="md",
                        c="white",
                        style={"letterSpacing": "-0.3px"}
                    ),
                    dmc.Text(
                        project["description"],
                        size="xs",
                        style=_CARD_BODY_TEXT_STYLE,
                        lineClamp=3,
                    ),
                ],
                p="md",
                style={"flex": 1, "display": "flex", "flexDirection": "column"},
            ),
        ],
        withBorder=False,
        shadow="md",
        radius="lg",
        style=card_style,
        className="card-hover",
    )

    return html.Div(card, id=project["id"], n_clicks=0, style={"height": "100%"})


def build_project_cards(projects: Iterable[dict]) -> List[html.Div]:
    """Return a list of project-card containers compatible with the grid (newest first)."""
    return [
        html.Div(create_project_card(project), style={"height": "100%"})
        for project in list(projects)
    ]


def build_engineering_cards(projects: Iterable[dict]) -> List[html.Div]:
    """Return a list of engineering-card containers for the grid."""
    return [create_engineering_card(project) for project in list(projects)]


def build_cards_grid(card_children: Iterable[html.Div]) -> dmc.SimpleGrid:
    """Wrap the provided card components in a scroll-snap coverflow layout."""
    items = [
        html.Div(
            html.Div(
                [
                    card,
                    html.Div(className="coverflow-shadow"),
                ],
                className="coverflow-surface",
            ),
            className="coverflow-item",
            **{"data-coverflow-item": "true"},
        )
        for card in list(card_children)
    ]

    return html.Div(
        className="coverflow-root",
        children=[
            html.Div(
                id="projects-coverflow-scroll",
                className="coverflow-scroll",
                children=items,
            ),
            dmc.Text(
                "Scroll horizontally to browse projects",
                c="dimmed",
                size="sm",
                ta="center",
                mt="md",
            ),
        ],
    )
