"""Application layout assembly."""

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify
from datetime import datetime, timezone

from .cards import build_project_cards, build_engineering_cards, build_cards_grid
from .data import CODING_PROJECTS, ENGINEERING_PROJECTS
from .modals import get_engineering_modals
from .theme import TAB_BUTTON_STYLE, PAGE_WRAPPER_STYLE, MANTINE_THEME


def _build_social_link(icon, href):
    return dmc.Anchor(
        DashIconify(icon=icon, width=28, color="#cbd5e1"),
        href=href,
        target="_blank",
        className="social-icon",
        style={
            "transition": "transform 0.2s, color 0.2s",
            "&:hover": {"transform": "scale(1.1)", "color": "#a855f7"}
        }
    )

def _build_profile_intro() -> html.Div:
    return dmc.Container(
        children=[
            dmc.SimpleGrid(
                cols=2,
                spacing="xl",
                className="hero-grid",
                children=[
                    dmc.Stack(
                        children=[
                            dmc.Badge(
                                "Available for Hire",
                                color="green",
                                variant="dot",
                                size="lg",
                                className="animate-fade-in"
                            ),
                            dmc.Title(
                                [
                                    "Building ",
                                    html.Span("Intelligent Systems", className="gradient-text"),
                                    " for the Real World."
                                ],
                                order=1,
                                size="3.5rem",
                                fw=800,
                                className="animate-fade-in-delay-1",
                                style={"lineHeight": 1.1, "letterSpacing": "-1px", "color": "white"}
                            ),
                            dmc.Text(
                                "Full Stack Engineer",
                                size="xl",
                                fw=500,
                                c="dimmed",
                                className="animate-fade-in-delay-2"
                            ),
                            dmc.Text(
                                "I bridge the gap between hardware realities and user experiences. "
                                "From autonomous perception pipelines to high-scale web infrastructure, "
                                "I design software that is reliable, scalable, and impactful.",
                                size="lg",
                                c="#94a3b8",
                                style={"maxWidth": "600px", "lineHeight": 1.6},
                                className="animate-fade-in-delay-2"
                            ),
                            dmc.Group(
                                children=[
                                    _build_social_link("skill-icons:linkedin", "https://www.linkedin.com/in/changyong-kwak-0b9385314/"),
                                    _build_social_link("ion:logo-github", "https://github.com/samkwak188"),
                                    dmc.Button(
                                        "View Projects",
                                        variant="gradient",
                                        gradient={"from": "indigo", "to": "cyan"},
                                        size="md",
                                        radius="xl",
                                        id="hero-cta-button"
                                    )
                                ],
                                gap="lg",
                                mt="xl",
                                className="animate-fade-in-delay-2"
                            )
                        ],
                        style={"height": "100%", "padding": "2rem 0"}
                    ),
                    dmc.Center(
                        children=[
                            dmc.Box(
                                className="animate-fade-in",
                                style={
                                    "position": "relative",
                                    "width": "300px",
                                    "height": "300px",
                                    "borderRadius": "50%",
                                    "background": "linear-gradient(45deg, #6366f1, #a855f7)",
                                    "padding": "4px",
                                    "boxShadow": "0 20px 50px rgba(99, 102, 241, 0.3)"
                                },
                                children=[
                                    dmc.Avatar(
                                        src="/assets/profile.png",
                                        size="100%",
                                        radius="50%",
                                        style={"border": "4px solid #0f172a"}
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ],
        size="lg",
        py=60
    )


def _build_landing_content() -> html.Div:
    return html.Div(
        _build_profile_intro(),
        style={
            "position": "relative",
            "minHeight": "80vh",
            "display": "flex",
            "alignItems": "center"
        },
    )


def _build_feature_item(title, description, icon):
    return dmc.Paper(
        p="xl",
        radius="lg",
        className="glass-card",
        children=[
            dmc.ThemeIcon(
                DashIconify(icon=icon, width=24),
                size=48,
                radius="md",
                variant="light",
                color="violet",
                mb="md"
            ),
            dmc.Text(title, size="lg", fw=700, c="white", mb="sm"),
            dmc.Text(description, size="sm", c="dimmed", style={"lineHeight": 1.6})
        ]
    )


def _build_about_content() -> html.Div:
    return dmc.Container(
        size="lg",
        py=40,
        children=[
            dmc.Title("Beyond the Code", order=2, c="white", mb="xl", ta="center"),
            dmc.SimpleGrid(
                cols=3,
                spacing="xl",
                className="feature-grid",
                children=[
                    _build_feature_item(
                        "Cross-Discipline Execution",
                        "I don't just write code; I build systems. My background spans robotics hardware, embedded C, and modern full-stack web architectures that integrate AI agents and APIs. I understand the entire stack, from the sensor to the screen.",
                        "carbon:ibm-cloud-pak-integration"
                    ),
                    _build_feature_item(
                        "Data-Driven Design",
                        "Intuition is good; data is better. I leverage analytics, gradient-boosting models, and rigorous testing to ensure my solutions aren't just functional—they're optimized for real-world performance.",
                        "carbon:chart-line-data"
                    ),
                    _build_feature_item(
                        "Product Mindset",
                        "I build for users, not just engineers. Whether it's a rental inspection tool or a video generation pipeline, I focus on clean UX, clear documentation, and solving the actual business problem.",
                        "carbon:user-activity"
                    )
                ]
            ),
            dmc.Blockquote(
                "I care about measurable impact, tight execution, and human-centric polish, whether the interface lives in a browser or on a physical device.",
                cite="- Changyong Kwak",
                mt=60,
                color="violet",
                style={"maxWidth": "800px", "margin": "60px auto", "background": "transparent", "borderLeft": "4px solid #8b5cf6"}
            )
        ]
    )


def _build_resume_section() -> html.Div:
    return html.Div(
        [
            dmc.Center(
                html.Iframe(
                    src="https://drive.google.com/file/d/1PRW91Kvkta2B1gPsh-zwzQw68E3U4qsu/preview",
                    style={
                        "width": "100%",
                        "maxWidth": "900px",
                        "height": "800px",
                        "border": "none",
                        "borderRadius": "12px",
                        "boxShadow": "0 10px 30px rgba(0,0,0,0.3)"
                    }
                )
            )
        ],
        style={
            "padding": "40px 0",
            "width": "100%",
        },
    )


def _build_projects_section():
    coding_cards = build_project_cards(CODING_PROJECTS)
    initial_grid = build_cards_grid(coding_cards)

    return dmc.Stack(
        children=[
            dmc.Group(
                justify="center",
                mb=40,
                children=[
                    dmc.SegmentedControl(
                        id="project-category-toggle",
                        value="coding",
                        data=[
                            {"label": "Software & AI", "value": "coding"},
                            {"label": "Robotics & Hardware", "value": "engineering"},
                        ],
                        size="md",
                        radius="xl",
                        classNames={"root": "glass-card"},
                        styles={
                            "root": {
                                "backgroundColor": "rgba(15, 23, 42, 0.6)",
                                "border": "1px solid rgba(255,255,255,0.1)",
                            },
                            "label": {"color": "#94a3b8", "fontWeight": 500},
                            "active": {"background": "linear-gradient(135deg, #6366f1, #8b5cf6)"}
                        }
                    )
                ]
            ),
            html.Div(
                initial_grid,
                id="projects-grid",
                style={"width": "100%"},
            ),
        ],
        style={"padding": "40px 0", "maxWidth": "1200px", "margin": "0 auto"}
    )


def _build_primary_tabs():
    return dmc.Tabs(
        [
            dmc.TabsList(
                [
                    dmc.TabsTab("Home", value="landing", className="primary-tab"),
                    dmc.TabsTab("About", value="about", className="primary-tab"),
                    dmc.TabsTab("Projects", value="projects", className="primary-tab"),
                    dmc.TabsTab("Resume", value="resume", className="primary-tab"),
                ],
                justify="center",
                className="primary-tabs"
            ),
            dmc.TabsPanel(_build_landing_content(), value="landing"),
            dmc.TabsPanel(_build_about_content(), value="about"),
            dmc.TabsPanel(_build_projects_section(), value="projects"),
            dmc.TabsPanel(_build_resume_section(), value="resume"),
        ],
        id="primary-tabs",
        value="landing",
        variant="pills",
        style={"marginTop": "20px"}
    )


def build_layout() -> dmc.MantineProvider:
    """Create the full Dash layout tree."""
    engineering_modals = get_engineering_modals()

    main_content = dmc.Container(
        [
            dmc.Text(
                f"Build: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC",
                size="xs",
                c="dimmed",
                style={"textAlign": "right", "marginTop": "8px"},
            ),
            _build_primary_tabs()
        ],
        fluid=True,
        style={"padding": "0 20px", "maxWidth": "1400px", "margin": "0 auto"}
    )

    return dmc.MantineProvider(
        theme=MANTINE_THEME,
        withCssVariables=True,
        withGlobalClasses=True,
        children=[
            *engineering_modals,
            html.Div(main_content, style=PAGE_WRAPPER_STYLE),
        ],
    )
