"""Single-page portfolio layout."""

from datetime import datetime

import dash_mantine_components as dmc
from dash import html

from .cards import build_cards_grid, build_project_cards
from .data import CODING_PROJECTS, CONTACT, EXPERIENCE, FEATURED_WORK, SKILLS
from .modals import get_engineering_modals
from .theme import MANTINE_THEME


def _external_props(is_external=True):
    if not is_external:
        return {}
    return {"target": "_blank", "rel": "noopener noreferrer"}


def _text_link(label, href, *, external=True, class_name="text-link"):
    return html.A(
        [label, html.Span("↗" if external else "↓", className="link-arrow")],
        href=href,
        className=class_name,
        **_external_props(external),
    )


def _section_heading(title, intro=None):
    children = [html.H2(title, className="section-title")]
    if intro:
        children.append(html.P(intro, className="section-intro"))
    return html.Header(children, className="section-heading")


def _navigation():
    return html.Header(
        html.Nav(
            [
                html.A("Changyong Kwak", href="#top", className="brand"),
                html.Div(
                    [
                        html.A("About", href="#about", className="nav-about"),
                        html.A("Work", href="#work", className="nav-work"),
                        html.A("Experience", href="#experience", className="nav-experience"),
                        html.A("Projects", href="#projects", className="nav-projects"),
                        html.A("Resume", href=CONTACT["resume"], target="_blank", className="nav-resume"),
                    ],
                    className="nav-links",
                ),
            ],
            className="nav-inner",
            **{"aria-label": "Main navigation"},
        ),
        className="site-header",
    )


def _hero():
    return html.Section(
        [
            html.Div(
                [
                    html.H1(
                        "I build dependable software for systems that have to work.",
                        className="hero-title",
                    ),
                    html.P(
                        "I'm Changyong Kwak, a computer science student at UW-Madison. "
                        "I build control tools, test infrastructure, and developer systems "
                        "across robotics and AI.",
                        className="hero-copy",
                    ),
                    html.Div(
                        [
                            html.A("See selected work", href="#work", className="button button-primary"),
                            html.A(
                                "Download resume",
                                href=CONTACT["resume"],
                                target="_blank",
                                className="button button-secondary",
                            ),
                        ],
                        className="hero-actions",
                    ),
                    html.P(
                        [
                            html.Span(className="availability-dot"),
                            "Seeking Winter and Summer 2027 software engineering internships.",
                        ],
                        className="availability",
                    ),
                ],
                className="hero-content",
            ),
            html.Figure(
                [
                    html.Div(
                        html.Img(
                            src="/assets/profile.png",
                            alt="Changyong Kwak at the Cursor Hackathon",
                            className="hero-photo",
                        ),
                        className="hero-photo-frame",
                    ),
                    html.Figcaption(
                        [
                            html.Span("Madison, Wisconsin"),
                            html.Span("Cursor Hackathon, 2026"),
                        ]
                    ),
                ],
                className="hero-figure",
            ),
        ],
        id="top",
        className="hero section-shell",
    )


def _flow_diagram(nodes):
    children = []
    for index, node in enumerate(nodes):
        children.append(html.Div(node, className="flow-node"))
        if index < len(nodes) - 1:
            children.append(html.Div("→", className="flow-arrow", **{"aria-hidden": "true"}))
    return html.Div(
        children,
        className="flow-diagram",
        **{"aria-label": "System flow: " + " to ".join(nodes)},
    )


def _featured_work_item(project):
    return html.Article(
        [
            html.Div(
                [
                    html.H3(project["title"]),
                    html.P(project["context"], className="work-context"),
                    html.P(project["summary"], className="work-summary"),
                    _text_link(
                        project["link_label"],
                        project["link"],
                        external=project["external"],
                    ),
                ],
                className="work-copy",
            ),
            html.Div(
                [
                    _flow_diagram(project["flow"]),
                    html.P("Failure-aware from input to result", className="diagram-caption"),
                ],
                className="work-diagram",
            ),
        ],
        className="featured-work-item",
    )


def _work_section():
    return html.Section(
        [
            _section_heading(
                "Selected work",
                "A few systems I can explain from the API down to the failure cases.",
            ),
            html.Div([_featured_work_item(project) for project in FEATURED_WORK]),
        ],
        id="work",
        className="content-section section-shell",
    )


def _experience_item(item):
    return html.Article(
        [
            html.Div(className="timeline-marker"),
            html.Div(
                [
                    html.H3(item["company"]),
                    html.P(item["role"], className="experience-role"),
                    html.P(item["description"], className="experience-description"),
                ],
                className="experience-main",
            ),
            html.Time(item["dates"], className="experience-dates"),
        ],
        className="experience-item",
    )


def _experience_section():
    return html.Section(
        [
            _section_heading("Experience"),
            html.Div([_experience_item(item) for item in EXPERIENCE], className="timeline"),
        ],
        id="experience",
        className="content-section section-shell",
    )


def _project_archive_section():
    initial_grid = build_cards_grid(build_project_cards(CODING_PROJECTS))
    return html.Section(
        [
            _section_heading(
                "Project archive",
                "Software, robotics, and hardware projects from the last several years.",
            ),
            html.Div(
                dmc.SegmentedControl(
                    id="project-category-toggle",
                    value="coding",
                    data=[
                        {"label": "Software and AI", "value": "coding"},
                        {"label": "Robotics and hardware", "value": "engineering"},
                    ],
                    className="archive-toggle",
                    size="md",
                ),
                className="archive-controls",
            ),
            html.Div(initial_grid, id="projects-grid", className="archive-grid"),
        ],
        id="projects",
        className="content-section project-archive-section",
    )


def _skill_column(title, skills):
    return html.Div(
        [html.H3(title), html.P("\n".join(skills), className="skill-list")],
        className="skill-column",
    )


def _about_section():
    return html.Section(
        [
            _section_heading("About"),
            html.Div(
                [
                    html.P(
                        "I like the parts of software where good behavior depends on careful "
                        "boundaries: a canceled robot command, an interrupted evaluation run, "
                        "or a tool that must fail safely.",
                        className="about-statement",
                    ),
                    html.Div(
                        [
                            html.P(
                                "At UW-Madison, I study computer science and work across robotics, "
                                "AI systems, and full-stack software. I enjoy tracing a problem "
                                "through the whole stack, then writing the tests that make the fix stick."
                            ),
                            html.P(
                                "I expect to graduate in December 2027. Outside class, I am usually "
                                "building a project, reading through an unfamiliar codebase, or helping "
                                "a teammate turn a rough demo into something reliable."
                            ),
                        ],
                        className="about-copy",
                    ),
                ],
                className="about-grid",
            ),
            html.Div(
                [_skill_column(title, skills) for title, skills in SKILLS.items()],
                className="skills-grid",
            ),
        ],
        id="about",
        className="content-section section-shell",
    )


def _contact_section():
    return html.Section(
        html.Div(
            [
                html.P("Have a role where this kind of work matters? I'd be glad to talk."),
                html.Div(
                    [
                        _text_link("Email", CONTACT["email"], external=False),
                        _text_link("LinkedIn", CONTACT["linkedin"]),
                        _text_link("GitHub", CONTACT["github"]),
                        _text_link("Resume", CONTACT["resume"]),
                    ],
                    className="contact-links",
                ),
            ],
            className="contact-block",
        ),
        className="contact-section section-shell",
    )


def _footer():
    return html.Footer(
        [
            html.P(f"Changyong Kwak · Madison, Wisconsin · {datetime.now().year}"),
            html.A("Back to top ↑", href="#top"),
        ],
        className="site-footer section-shell",
    )


def build_layout():
    """Create the full Dash layout tree."""
    return dmc.MantineProvider(
        theme=MANTINE_THEME,
        withCssVariables=True,
        withGlobalClasses=True,
        children=[
            html.A("Skip to main content", href="#about", className="skip-link"),
            *get_engineering_modals(),
            _navigation(),
            html.Main(
                [
                    _hero(),
                    _about_section(),
                    _work_section(),
                    _experience_section(),
                    _project_archive_section(),
                    _contact_section(),
                ]
            ),
            _footer(),
        ],
    )
