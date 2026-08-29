"""Reusable cards for the horizontal project archive."""

from typing import Iterable, List

from dash import html


def _project_links(project):
    links = []
    for label, key in (("Demo", "demo_url"), ("Live site", "live_url"), ("Repository", "github_url")):
        url = project.get(key)
        if not url:
            continue
        links.append(
            html.A(
                label,
                href=url,
                target="_blank",
                rel="noopener noreferrer",
                className="project-card-link",
            )
        )
    return links


def _project_image(project, *, eager=False):
    image_props = {
        "alt": project["image_alt"],
        "className": "project-card-image",
    }
    if project.get("image_position"):
        image_props["style"] = {"objectPosition": project["image_position"]}
    if eager:
        image_props["src"] = project["image_src"]
    else:
        image_props["data-lazy-src"] = project["image_src"]
    media_class = "project-card-media"
    if project.get("image_fit") == "contain":
        media_class += " project-card-media-contain"
    return html.Div(
        html.Img(**image_props),
        className=media_class,
    )


def _project_meta(project):
    stack = project.get("stack", [])
    return html.Div(
        [
            html.P(project.get("context", "Independent project"), className="project-card-context"),
            html.P(" · ".join(stack), className="project-card-stack") if stack else None,
        ],
        className="project-card-meta",
    )


def create_project_card(project: dict, *, eager=False) -> html.Article:
    """Return a software project card."""
    return html.Article(
        [
            html.Header(
                [
                    html.H3(project["title"], className="project-card-title"),
                    _project_meta(project),
                ],
                className="project-card-header",
            ),
            _project_image(project, eager=eager),
            html.Div(
                [
                    html.P(project["description"], className="project-card-description"),
                    html.Div(_project_links(project), className="project-card-links"),
                ],
                className="project-card-body",
            ),
        ],
        className="project-card",
    )


def create_engineering_card(project: dict) -> html.Button:
    """Return a keyboard-accessible hardware project card that opens its detail modal."""
    return html.Button(
        [
            html.Article(
                [
                    html.Header(
                        [
                            html.H3(project["title"], className="project-card-title"),
                            _project_meta(project),
                        ],
                        className="project-card-header",
                    ),
                    _project_image(project, eager=False),
                    html.Div(
                        [
                            html.P(project["description"], className="project-card-description"),
                            html.Span("Open project details", className="project-card-link"),
                        ],
                        className="project-card-body",
                    ),
                ],
                className="project-card engineering-project-card",
            )
        ],
        id=project["id"],
        n_clicks=0,
        type="button",
        className="engineering-card-trigger",
        **{"aria-label": f"Open details for {project['title']}"},
    )


def build_project_cards(projects: Iterable[dict]) -> List[html.Article]:
    return [
        create_project_card(project, eager=index < 3)
        for index, project in enumerate(list(projects))
    ]


def build_engineering_cards(projects: Iterable[dict]) -> List[html.Button]:
    return [create_engineering_card(project) for project in list(projects)]


def build_cards_grid(card_children: Iterable) -> html.Div:
    """Preserve the original scroll-snap coverflow interaction."""
    items = [
        html.Div(
            html.Div(
                [card, html.Div(className="coverflow-shadow")],
                className="coverflow-surface",
            ),
            className="coverflow-item",
            **{
                "data-coverflow-item": "true",
                "data-coverflow-index": str(index),
                "role": "group",
            },
        )
        for index, card in enumerate(list(card_children))
    ]
    return html.Div(
        [
            html.Div(
                items,
                id="projects-coverflow-scroll",
                className="coverflow-scroll",
                tabIndex=0,
                **{
                    "aria-label": "Scrollable project archive",
                    "aria-roledescription": "carousel",
                },
            ),
            html.Div(
                [
                    html.Button("Previous", type="button", className="coverflow-button coverflow-prev"),
                    html.P("Drag, scroll, or use the arrow keys to browse.", className="coverflow-hint"),
                    html.Button("Next", type="button", className="coverflow-button coverflow-next"),
                ],
                className="coverflow-controls",
            ),
        ],
        className="coverflow-root",
    )
