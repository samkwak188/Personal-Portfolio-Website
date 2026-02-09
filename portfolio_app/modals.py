"""Modal components describing engineering projects in detail."""

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify


def _build_section_header(text, icon):
    return dmc.Group(
        [
            dmc.ThemeIcon(
                DashIconify(icon=icon, width=20),
                size="lg",
                radius="xl",
                variant="gradient",
                gradient={"from": "indigo", "to": "cyan"},
            ),
            dmc.Text(text, fw=700, size="lg", c="white"),
        ],
        mb="sm",
        mt="xl",
    )


def _build_list_item(text):
    return dmc.Group(
        align="start",
        gap="sm",
        mb="xs",
        children=[
            dmc.ThemeIcon(
                DashIconify(icon="material-symbols:check-circle-outline-rounded", width=16),
                size="sm",
                variant="light",
                color="cyan",
                radius="xl",
                mt=2
            ),
            dmc.Text(text, size="sm", c="dimmed", style={"flex": 1, "lineHeight": 1.5}),
        ]
    )


def _build_modal_layout(image_src, content_sections):
    # dash-mantine-components==0.12.1 does not expose Grid/Col the same way newer versions do.
    # Use SimpleGrid for a responsive 2-column layout instead (1 column on small screens).
    return dmc.SimpleGrid(
        cols=2,
        spacing="xl",
        className="engineering-modal-grid",
        children=[
            dmc.Image(
                src=image_src,
                radius="lg",
                className="glass-card",
                style={"border": "1px solid rgba(255,255,255,0.1)"},
            ),
            dmc.Stack(
                gap="sm",
                style={"maxHeight": "70vh", "overflowY": "auto", "paddingRight": "10px"},
                children=content_sections,
            ),
        ],
    )


def get_engineering_modals() -> list[dmc.Modal]:
    return [
        # Modal 1: Kitchen Wastewater Purifier
        dmc.Modal(
            title=dmc.Text("Kitchen Wastewater Purifier", size="xl", fw=700, variant="gradient", gradient={"from": "blue", "to": "cyan"}),
            id="modal-1",
            size="80%",
            zIndex=10000,
            overlayProps={"opacity": 0.55, "blur": 3},
            styles={
                "modal": {"backgroundColor": "#0f172a", "border": "1px solid rgba(255,255,255,0.1)"},
                "header": {"backgroundColor": "#0f172a"},
                "body": {"padding": "20px"},
            },
            children=_build_modal_layout(
                "https://i.im.ge/2025/02/03/HdWsmz.prof-thumbnail-2.png",
                [
                    _build_section_header("The Problem", "carbon:warning-alt"),
                    dmc.Text(
                        "Kitchen wastewater from Malaysian households and restaurants contains high levels of oils and food particles. "
                        "Direct disposal leads to clogged sewers, unpleasant odors, and significant water waste.",
                        size="sm",
                        c="dimmed",
                        mb="lg"
                    ),
                    
                    _build_section_header("The Solution", "carbon:idea"),
                    dmc.Text(
                        "An innovative multi-stage filtration system that separates oils and particulates to recycle wastewater.",
                        size="sm",
                        c="dimmed",
                        mb="lg"
                    ),

                    _build_section_header("Key Features", "carbon:settings-check"),
                    dmc.Stack(
                        gap=4,
                        children=[
                            _build_list_item("Density-based oil separation with heating elements"),
                            _build_list_item("Rotating oil scraping disks"),
                            _build_list_item("Activated carbon & zeolite odor filtration"),
                            _build_list_item("Particle filtration for food residue"),
                        ]
                    ),

                    _build_section_header("Impact", "carbon:chart-line"),
                    dmc.Stack(
                        gap=4,
                        children=[
                            _build_list_item("Significantly reduces water waste"),
                            _build_list_item("Lowers utility costs for businesses"),
                            _build_list_item("Prevents sewer infrastructure damage"),
                        ]
                    ),
                ]
            ),
        ),

        # Modal 2: 4D Home Cinema Helmet
        dmc.Modal(
            title=dmc.Text("4D Home Cinema Helmet", size="xl", fw=700, variant="gradient", gradient={"from": "purple", "to": "pink"}),
            id="modal-2",
            size="80%",
            zIndex=10000,
            overlayProps={"opacity": 0.55, "blur": 3},
            styles={
                "modal": {"backgroundColor": "#0f172a", "border": "1px solid rgba(255,255,255,0.1)"},
                "header": {"backgroundColor": "#0f172a"},
                "body": {"padding": "20px"},
            },
            children=_build_modal_layout(
                "https://i.im.ge/2025/02/03/Hdkhza.prof-thumbnail-3.png",
                [
                    _build_section_header("Overview", "carbon:trophy"),
                    dmc.Text(
                        "First-place winner at the World Robot Olympiad Korea. Inspired by a friend with mobility disabilities, "
                        "this headset brings the immersive 4D cinema experience to those who cannot easily visit theaters.",
                        size="sm",
                        c="dimmed",
                        mb="lg"
                    ),

                    _build_section_header("Technology Stack", "carbon:code"),
                    dmc.Stack(
                        gap=4,
                        children=[
                            _build_list_item("Embedded C control systems"),
                            _build_list_item("Custom 3D-printed hardware integration"),
                            _build_list_item("Servo motor & pump synchronization"),
                        ]
                    ),

                    _build_section_header("Immersive Effects", "carbon:rain-drop"),
                    dmc.Stack(
                        gap=4,
                        children=[
                            _build_list_item("Rain simulation with micro-pumps"),
                            _build_list_item("Motion effects via crank & slider mechanisms"),
                            _build_list_item("Scent diffusion & mist generation"),
                            _build_list_item("Dynamic lighting synchronized with video"),
                        ]
                    ),
                ]
            ),
        ),

        # Modal 3: Dancing Humanoids
        dmc.Modal(
            title=dmc.Text("Dancing Humanoids", size="xl", fw=700, variant="gradient", gradient={"from": "orange", "to": "red"}),
            id="modal-3",
            size="80%",
            zIndex=10000,
            overlayProps={"opacity": 0.55, "blur": 3},
            styles={
                "modal": {"backgroundColor": "#0f172a", "border": "1px solid rgba(255,255,255,0.1)"},
                "header": {"backgroundColor": "#0f172a"},
                "body": {"padding": "20px"},
            },
            children=_build_modal_layout(
                "https://i.im.ge/2025/02/04/HqPpyL.prof-thumbnail-4.png",
                [
                    _build_section_header("Technical Implementation", "carbon:bot"),
                    dmc.Stack(
                        gap=4,
                        children=[
                            _build_list_item("Multi-servo motor control for full-body articulation"),
                            _build_list_item("Custom gait & dance sequence programming in C"),
                            _build_list_item("Synchronized multi-robot performance"),
                        ]
                    ),

                    _build_section_header("Community Impact", "carbon:group"),
                    dmc.Text(
                        "Performances at Chung-Jung Church and Holt School for the Disabled. "
                        "Used robotics as a medium for entertainment and STEM education.",
                        size="sm",
                        c="dimmed",
                        mb="lg"
                    ),

                    _build_section_header("Outcomes", "carbon:result"),
                    dmc.Stack(
                        gap=4,
                        children=[
                            _build_list_item("Demonstrated complex motor coordination"),
                            _build_list_item("Engaged diverse audiences with technology"),
                            _build_list_item("Bridged gap between engineering and art"),
                        ]
                    ),
                ]
            ),
        ),
    ]
