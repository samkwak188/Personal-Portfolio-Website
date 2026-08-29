"""Single-page portfolio layout."""

from datetime import datetime

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from .cards import build_cards_grid, build_engineering_cards, build_project_cards
from .data import ALL_PROJECTS, CONTACT, ENGINEERING_PROJECTS, EXPERIENCE, SKILL_GROUPS
from .modals import get_engineering_modals
from .theme import MANTINE_THEME


def _external_props(is_external=True):
    if not is_external:
        return {}
    return {"target": "_blank", "rel": "noopener noreferrer"}


def _section_heading(title, intro=None, *, inverse=False):
    children = [html.H2(title, className="section-title")]
    if intro:
        children.append(html.P(intro, className="section-intro"))
    classes = "section-heading section-heading-inverse" if inverse else "section-heading"
    return html.Header(children, className=classes)


def _navigation():
    return html.Header(
        html.Nav(
            [
                html.A("Changyong Kwak", href="#top", className="brand"),
                html.Button(
                    "Menu",
                    id="menu-toggle",
                    className="menu-toggle",
                    type="button",
                    **{
                        "aria-controls": "primary-navigation",
                        "aria-expanded": "false",
                    },
                ),
                html.Div(
                    [
                        html.A("About", href="#about"),
                        html.A("Projects", href="#projects"),
                        html.A("Experience", href="#experience"),
                        html.A("Contact", href="#contact"),
                    ],
                    id="primary-navigation",
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
            html.Canvas(
                id="spatial-field",
                className="spatial-field",
                **{"aria-hidden": "true"},
            ),
            html.Div(
                html.Div(
                    [
                        html.H1(
                            [
                                html.Span(
                                    "I build dependable",
                                    className="hero-title-line",
                                ),
                                html.Span(
                                    "software for systems",
                                    className="hero-title-line",
                                ),
                                html.Span(
                                    "that have to work.",
                                    className="hero-title-line",
                                ),
                            ],
                            className="hero-title",
                        ),
                        html.P(
                            "Software engineer working across robotics, developer "
                            "infrastructure, and reliable intelligent systems.",
                            className="hero-copy",
                        ),
                        html.Div(
                            [
                                html.A(
                                    "Explore projects",
                                    href="#projects",
                                    className="hero-link",
                                ),
                                html.A("Contact", href="#contact", className="hero-link"),
                            ],
                            className="hero-actions",
                        ),
                        html.P(
                            "Seeking Winter and Summer 2027 software engineering internships.",
                            className="availability",
                        ),
                    ],
                    className="hero-content",
                ),
                className="hero-inner section-shell",
            ),
        ],
        id="top",
        className="hero",
    )


def _about_section():
    return html.Section(
        html.Div(
            html.Div(
                [
                    html.Div(
                        [
                            html.H2("About", className="about-title"),
                            html.P(
                                "I am Changyong Kwak, a computer science student at "
                                "UW-Madison and a software engineer working across product "
                                "interfaces, backend systems, robotics, and applied machine "
                                "learning. I care most about software whose behavior can be "
                                "explained, tested, and trusted - from browser-to-robot control "
                                "and evaluation infrastructure to security tools and focused "
                                "products built under real constraints.",
                                className="about-intro",
                            ),
                        ],
                        className="about-copy",
                    ),
                    html.Figure(
                        html.Img(
                            src="/assets/profile.png",
                            alt=(
                                "Changyong Kwak beside the Cursor banner at the "
                                "Cursor Hackathon"
                            ),
                            className="about-photo",
                        ),
                        className="about-figure",
                    ),
                ],
                className="about-layout",
            ),
            className="section-shell",
        ),
        id="about",
        className="about-section",
    )


def _skill_tab(group, index):
    selected = index == 0
    return html.Button(
        [
            DashIconify(icon=group["icon"], width=24, height=24),
            html.Span(group["label"]),
        ],
        id=f"skill-tab-{group['id']}",
        type="button",
        className="skill-tab is-active" if selected else "skill-tab",
        **{
            "data-skill-control": group["id"],
            "role": "tab",
            "aria-selected": "true" if selected else "false",
            "aria-controls": f"skill-panel-{group['id']}",
            "tabIndex": 0 if selected else -1,
        },
    )


def _skill_panel(group, index):
    return html.Div(
        [
            html.P(group["description"], className="skill-panel-copy"),
            html.Ul(
                [html.Li(item) for item in group["items"]],
                className="skill-tool-list",
            ),
        ],
        id=f"skill-panel-{group['id']}",
        className="skill-panel is-active" if index == 0 else "skill-panel",
        **{
            "data-skill-panel": group["id"],
            "role": "tabpanel",
            "aria-labelledby": f"skill-tab-{group['id']}",
            "aria-hidden": "false" if index == 0 else "true",
        },
    )


def _skills_section():
    return html.Section(
        html.Div(
            [
                _section_heading(
                    "Tools and systems",
                    "Select a discipline to see the technologies I use and how I approach the work.",
                    inverse=True,
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                _skill_tab(group, index)
                                for index, group in enumerate(SKILL_GROUPS)
                            ],
                            className="skill-tabs",
                            **{"role": "tablist", "aria-label": "Technical disciplines"},
                        ),
                        html.Div(
                            [
                                _skill_panel(group, index)
                                for index, group in enumerate(SKILL_GROUPS)
                            ],
                            className="skill-stage",
                            **{"data-skill-stage": "true"},
                        ),
                    ],
                    className="skills-instrument",
                    **{"data-skills-instrument": "true"},
                ),
            ],
            className="section-shell",
        ),
        className="skills-section",
    )


def _work_section():
    archive_cards = [
        *build_project_cards(ALL_PROJECTS),
        *build_engineering_cards(ENGINEERING_PROJECTS),
    ]
    return html.Section(
        [
            html.Div(
                _section_heading(
                    "Projects",
                    "The complete archive: product software, research systems, robotics, and physical prototypes.",
                ),
                className="projects-heading section-shell",
            ),
            html.Div(
                build_cards_grid(archive_cards),
                id="projects-grid",
                className="archive-grid",
            ),
        ],
        id="projects",
        className="projects-section",
    )


def _experience_item(item):
    return html.Article(
        [
            html.Div(
                [
                    html.H3(item["company"]),
                    html.P(item["role"], className="experience-role"),
                ],
                className="experience-title-block",
            ),
            html.Time(item["dates"], className="experience-dates"),
            html.P(item["description"], className="experience-description"),
        ],
        className="experience-item",
    )


def _experience_section():
    return html.Section(
        html.Div(
            [
                _section_heading(
                    "Experience",
                    "Engineering work where reliability, evidence, and clear failure behavior matter.",
                    inverse=True,
                ),
                html.Div(
                    [_experience_item(item) for item in EXPERIENCE],
                    className="experience-list",
                ),
            ],
            className="section-shell",
        ),
        id="experience",
        className="experience-section",
    )


def _contact_link(label, href, icon, *, external=True):
    return html.A(
        [
            DashIconify(icon=icon, width=28, height=28),
            html.Span(label),
        ],
        href=href,
        className="contact-link",
        **_external_props(external),
    )


def _contact_section():
    return html.Section(
        html.Div(
            [
                html.Div(
                    [
                        html.H2("Contact", className="contact-title"),
                        html.P(
                            "If you are building software where the details matter, "
                            "I would be glad to hear about it.",
                            className="contact-copy",
                        ),
                    ],
                    className="contact-heading",
                ),
                html.Div(
                    [
                        _contact_link(
                            "LinkedIn",
                            CONTACT["linkedin"],
                            "simple-icons:linkedin",
                        ),
                        _contact_link(
                            "GitHub",
                            CONTACT["github"],
                            "simple-icons:github",
                        ),
                        _contact_link(
                            "Email",
                            CONTACT["email"],
                            "ph:envelope-simple",
                            external=False,
                        ),
                        _contact_link(
                            "Resume",
                            CONTACT["resume"],
                            "ph:file-text",
                        ),
                    ],
                    className="contact-links",
                    **{"aria-label": "Contact links"},
                ),
            ],
            className="contact-inner section-shell",
        ),
        id="contact",
        className="contact-section",
    )


def _footer():
    return html.Footer(
        html.Div(
            [
                html.P(
                    f"Changyong Kwak · Madison, Wisconsin · {datetime.now().year}"
                ),
                html.A("Back to top", href="#top"),
            ],
            className="footer-inner section-shell",
        ),
        className="site-footer",
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
                    _skills_section(),
                    _work_section(),
                    _experience_section(),
                    _contact_section(),
                ],
                id="main-content",
            ),
            _footer(),
        ],
    )
