"""Application layout assembly."""

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify
from datetime import datetime, timezone

from .cards import build_project_cards, build_engineering_cards, build_cards_grid
from .data import CODING_PROJECTS, ENGINEERING_PROJECTS, IMPACT_METRICS, TECH_STACK
from .modals import get_engineering_modals
from .theme import TAB_BUTTON_STYLE, PAGE_WRAPPER_STYLE, MANTINE_THEME


def _build_social_link(icon, href):
    return dmc.Anchor(
        DashIconify(icon=icon, width=24, color="#cbd5e1"),
        href=href,
        target="_blank",
        className="social-icon",
    )


def _build_section_heading(kicker, title, subtitle=None):
    return dmc.Stack(
        gap=6,
        mb="xl",
        children=[
            dmc.Text(kicker, className="section-kicker"),
            dmc.Title(title, order=2, c="white", className="glow-text"),
            dmc.Text(subtitle, c="#94a3b8", size="sm") if subtitle else None,
        ],
    )


def _build_metric_chips():
    return dmc.Group(
        gap="sm",
        mt="lg",
        children=[
            dmc.Paper(
                className="metric-chip",
                radius="xl",
                px="md",
                py="xs",
                children=[
                    dmc.Text(metric["value"], fw=700, c="white", size="sm"),
                    dmc.Text(metric["label"], size="xs", c="#94a3b8"),
                ],
            )
            for metric in IMPACT_METRICS
        ],
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
                                className="animate-fade-in",
                                styles={
                                    "root": {"backgroundColor": "rgba(20, 83, 45, 0.2)", "border": "1px solid rgba(34, 197, 94, 0.2)"},
                                    "label": {"color": "white"},
                                }
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
                                style={"lineHeight": 1.1, "letterSpacing": "-1px", "color": "white", "marginBottom": "16px"}
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
                            _build_metric_chips(),
                            dmc.Group(
                                children=[
                                    dmc.Button(
                                        "View Projects",
                                        variant="gradient",
                                        gradient={"from": "indigo", "to": "cyan"},
                                        size="md",
                                        radius="xl",
                                        id="hero-cta-button",
                                        rightSection=DashIconify(icon="formkit:arrow-right", width=16),
                                        className="animate-fade-in-delay-2"
                                    ),
                                    dmc.Group(
                                        gap="xs",
                                        children=[
                                            _build_social_link("skill-icons:linkedin", "https://www.linkedin.com/in/changyong-kwak-0b9385314/"),
                                            _build_social_link("ion:logo-github", "https://github.com/samkwak188"),
                                        ],
                                        className="animate-fade-in-delay-2"
                                    )
                                ],
                                gap="xl",
                                mt="xl",
                                align="center"
                            )
                        ],
                        style={"height": "100%", "padding": "2rem 0", "justifyContent": "center"}
                    ),
                    dmc.Center(
                        style={"transform": "translateY(-90px)"},
                        children=[
                            dmc.Box(
                                className="animate-fade-in",
                                style={
                                    "position": "relative",
                                    "width": "320px",
                                    "height": "320px",
                                    "borderRadius": "50%",
                                    "background": "linear-gradient(135deg, rgba(99, 102, 241, 0.5), rgba(168, 85, 247, 0.5))",
                                    "padding": "6px",
                                    "boxShadow": "0 20px 60px rgba(99, 102, 241, 0.25)",
                                    "transform": "translateY(-38px)",
                                },
                                children=[
                                    dmc.Avatar(
                                        src="/assets/profile.png",
                                        size="100%",
                                        radius="50%",
                                        style={"border": "6px solid #0f172a"}
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ],
        size="lg",
        py=80
    )


def _build_landing_content() -> html.Div:
    return html.Div(
        _build_profile_intro(),
        style={
            "position": "relative",
            "minHeight": "85vh",
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
                size=56,
                radius="md",
                variant="light",
                color="violet",
                mb="md",
                style={"backgroundColor": "rgba(139, 92, 246, 0.1)"}
            ),
            dmc.Text(title, size="lg", fw=700, c="white", mb="sm"),
            dmc.Text(description, size="sm", c="dimmed", style={"lineHeight": 1.6})
        ]
    )


def _build_about_content() -> html.Div:
    return dmc.Container(
        size="lg",
        py=60,
        children=[
            _build_section_heading(
                "Discovery",
                "Beyond the Code",
                "I design and ship systems at the intersection of AI, software engineering, and product execution. "
                "My focus is turning complex ideas into scalable systems that are reliable, measurable, and human-centered.",
            ),
            dmc.SimpleGrid(
                cols=3,
                spacing="xl",
                className="feature-grid",
                children=[
                    _build_feature_item(
                        "Cross-Discipline Execution",
                        "I build end-to-end systems across robotics hardware, embedded software, and full-stack web architecture.",
                        "carbon:ibm-cloud-pak-integration"
                    ),
                    _build_feature_item(
                        "Data-Driven Design",
                        "I use analytics, experimentation, and model-driven decisions to optimize reliability and outcomes.",
                        "carbon:chart-line-data"
                    ),
                    _build_feature_item(
                        "Product Mindset",
                        "I prioritize user clarity, business impact, and execution speed from prototype to production.",
                        "carbon:user-activity"
                    )
                ]
            ),
            dmc.Space(h=60),
            _build_section_heading(
                "Inventory",
                "The Tech Stack",
            ),
            dmc.SimpleGrid(
                cols=2,
                spacing="xl",
                className="tech-grid",
                children=[
                    dmc.Paper(
                        className="glass-card",
                        p="xl",
                        radius="lg",
                        children=[
                            dmc.Text(group["category"], fw=700, c="white", mb="md"),
                            dmc.Group(
                                gap="xs",
                                children=[
                                    dmc.Badge(
                                        item,
                                        variant="light",
                                        color="violet",
                                        radius="sm",
                                        className="tech-badge",
                                        size="lg"
                                    )
                                    for item in group["items"]
                                ],
                            ),
                        ],
                    )
                    for group in TECH_STACK
                ],
            ),
            dmc.Blockquote(
                "\"sometimes, the idea that seems the worst turns out to be the best.\"",
                cite="- Sam Altman",
                mt=60,
                color="violet",
                style={
                    "maxWidth": "900px",
                    "margin": "60px auto 0 auto",
                    "background": "transparent",
                    "borderLeft": "4px solid #8b5cf6",
                },
            ),
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
                        "boxShadow": "0 20px 50px rgba(0,0,0,0.5)"
                    }
                )
            )
        ],
        style={
            "padding": "60px 0",
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
                mb=50,
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
        style={"padding": "40px 0", "maxWidth": "1380px", "margin": "0 auto"}
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
        style={"marginTop": "30px"}
    )


def _build_footer():
    return dmc.Container(
        size="lg",
        py="xl",
        mt="xl",
        style={"borderTop": "1px solid rgba(255,255,255,0.05)"},
        children=[
            dmc.Group(
                justify="space-between",
                children=[
                    dmc.Text(
                        "© 2026 Changyong Kwak. All rights reserved.",
                        size="sm",
                        c="dimmed"
                    ),
                    dmc.Group(
                        gap="xs",
                        children=[
                            dmc.Text("Built with", size="sm", c="dimmed"),
                            dmc.Badge("Python", size="xs", variant="outline", color="blue"),
                            dmc.Text("&", size="sm", c="dimmed"),
                            dmc.Badge("Dash", size="xs", variant="outline", color="cyan"),
                        ]
                    )
                ]
            )
        ]
    )


def build_layout() -> dmc.MantineProvider:
    """Create the full Dash layout tree."""
    engineering_modals = get_engineering_modals()

    main_content = dmc.Container(
        [
            dmc.Group(
                justify="space-between",
                align="center",
                mt="md",
                children=[
                    dmc.UnstyledButton(
                        dmc.Text("CK.", fw=900, size="xl", className="gradient-text", style={"letterSpacing": "-1px"}),
                        id="brand-home-button",
                        style={"cursor": "pointer"},
                    ),
                    dmc.Text(
                        f"Build: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC",
                        size="xs",
                        c="dimmed",
                        style={"opacity": 0.5}
                    ),
                ]
            ),
            _build_primary_tabs(),
            _build_footer()
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
