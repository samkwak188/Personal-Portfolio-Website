"""Reusable card component builders."""

from typing import Iterable, List

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from .theme import CARD_STYLE

_CARD_IMAGE_STYLE = {
    "height": "200px",
    "objectFit": "cover",
    "width": "100%",
    "borderTopLeftRadius": "12px",
    "borderTopRightRadius": "12px",
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
    anchor_href = (
        project.get("live_url")
        or project.get("demo_url")
        or project.get("detail_url")
        or project.get("github_url")
    )
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

    return dmc.Card(
        children=[
            dmc.CardSection(
                dmc.Anchor(
                    dmc.Image(
                        src=project["image_src"],
                        alt=project["image_alt"],
                        style=_CARD_IMAGE_STYLE,
                    ),
                    href=anchor_href,
                    target="_blank",
                ),
                style=_CARD_IMAGE_SECTION_STYLE,
            ),
            dmc.Stack(
                [
                    dmc.Text(
                        project["title"],
                        fw=700,
                        size="lg",
                        c="white",
                        style={"letterSpacing": "-0.5px"}
                    ),
                    dmc.Text(
                        project["description"],
                        size="sm",
                        style=_CARD_BODY_TEXT_STYLE,
                    ),
                    dmc.Box(
                        dmc.Group(buttons, gap="xs", wrap="wrap") if buttons else None,
                        style=_BUTTON_CONTAINER_STYLE,
                    ),
                ],
                p="lg",
                style={"flex": 1, "display": "flex", "flexDirection": "column"},
            ),
        ],
        withBorder=False,
        shadow="sm",
        radius="lg",
        style=CARD_STYLE,
        className="glass-card card-hover",
    )


def create_engineering_card(project: dict) -> html.Div:
    """Return an engineering project card wrapper with the expected ID."""
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
                        size="lg",
                        c="white",
                        style={"letterSpacing": "-0.5px"}
                    ),
                    dmc.Text(
                        project["description"],
                        size="sm",
                        style=_CARD_BODY_TEXT_STYLE,
                    ),
                ],
                p="lg",
                style={"flex": 1, "display": "flex", "flexDirection": "column"},
            ),
        ],
        withBorder=False,
        shadow="sm",
        radius="lg",
        style=dict(CARD_STYLE, cursor="pointer"),
        className="glass-card card-hover",
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
    """Wrap the provided card components in a responsive grid layout."""
    return dmc.SimpleGrid(
        cols=3,
        spacing="xl",
        verticalSpacing="xl",
        style=_GRID_STYLE,
        className="project-grid",
        children=list(card_children),
    )
