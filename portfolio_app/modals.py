"""Modal components describing engineering projects in detail."""

import dash_mantine_components as dmc
from dash_iconify import DashIconify


def _build_section_header(text, icon):
    return dmc.Group(
        [
            dmc.ThemeIcon(
                DashIconify(icon=icon, width=19),
                size="lg",
                radius=0,
                variant="outline",
                color="blue",
                className="modal-section-icon",
            ),
            dmc.Text(text, fw=600, size="lg", className="modal-section-title"),
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
                DashIconify(icon="carbon:checkmark", width=15),
                size="sm",
                variant="outline",
                color="blue",
                radius=0,
                mt=2,
            ),
            dmc.Text(text, size="sm", className="modal-body-copy", style={"flex": 1}),
        ],
    )


def _body_text(text):
    return dmc.Text(text, size="sm", className="modal-body-copy", mb="lg")


def _build_modal_layout(image_src, image_alt, content_sections):
    return dmc.SimpleGrid(
        cols={"base": 1, "md": 2},
        spacing="xl",
        className="engineering-modal-grid",
        children=[
            dmc.Image(
                src=image_src,
                alt=image_alt,
                radius=0,
                className="engineering-modal-image",
            ),
            dmc.Stack(
                gap="sm",
                className="engineering-modal-copy",
                children=content_sections,
            ),
        ],
    )


def _modal(title, modal_id, image_src, image_alt, sections):
    return dmc.Modal(
        title=dmc.Text(title, className="engineering-modal-title"),
        id=modal_id,
        size="80%",
        zIndex=10000,
        radius=0,
        overlayProps={"backgroundOpacity": 0.72, "blur": 4},
        className="engineering-modal",
        styles={
            "content": {"backgroundColor": "#f1eee6", "border": "1px solid #bdb9ae"},
            "header": {"backgroundColor": "#f1eee6", "padding": "22px 24px"},
            "body": {"padding": "0 24px 28px"},
        },
        children=_build_modal_layout(image_src, image_alt, sections),
    )


def get_engineering_modals() -> list[dmc.Modal]:
    return [
        _modal(
            "Kitchen Wastewater Purifier",
            "modal-1",
            "/assets/kitchen.png",
            "Kitchen wastewater purifier prototype",
            [
                _build_section_header("The problem", "carbon:warning-alt"),
                _body_text(
                    "Kitchen wastewater from Malaysian households and restaurants contains high "
                    "levels of oils and food particles. Direct disposal leads to clogged sewers, "
                    "unpleasant odors, and significant water waste."
                ),
                _build_section_header("The solution", "carbon:idea"),
                _body_text(
                    "A multi-stage filtration system that separates oil and food particles so the "
                    "water can be reused."
                ),
                _build_section_header("Key features", "carbon:settings-check"),
                dmc.Stack(
                    gap=4,
                    children=[
                        _build_list_item("Density-based oil separation with heating elements"),
                        _build_list_item("Rotating oil scraping disks"),
                        _build_list_item("Activated carbon and zeolite odor filtration"),
                        _build_list_item("Particle filtration for food residue"),
                    ],
                ),
                _build_section_header("Impact", "carbon:chart-line"),
                dmc.Stack(
                    gap=4,
                    children=[
                        _build_list_item("Reuses water that would otherwise enter the drain"),
                        _build_list_item("Removes oil before it reaches household plumbing"),
                        _build_list_item("Uses replaceable carbon and zeolite filter media"),
                    ],
                ),
            ],
        ),
        _modal(
            "4D Home Cinema Helmet",
            "modal-2",
            "/assets/4dhelmet.png",
            "4D home cinema helmet prototype",
            [
                _build_section_header("Overview", "carbon:trophy"),
                _body_text(
                    "First-place winner at the World Robot Olympiad Korea. Inspired by a friend "
                    "with mobility disabilities, this headset brings an immersive cinema experience "
                    "to people who cannot easily visit theaters."
                ),
                _build_section_header("Technology", "carbon:code"),
                dmc.Stack(
                    gap=4,
                    children=[
                        _build_list_item("Embedded C control systems"),
                        _build_list_item("Custom 3D-printed hardware integration"),
                        _build_list_item("Servo motor and pump synchronization"),
                    ],
                ),
                _build_section_header("Immersive effects", "carbon:rain-drop"),
                dmc.Stack(
                    gap=4,
                    children=[
                        _build_list_item("Rain simulation with micro-pumps"),
                        _build_list_item("Motion effects via crank and slider mechanisms"),
                        _build_list_item("Scent diffusion and mist generation"),
                        _build_list_item("Dynamic lighting synchronized with video"),
                    ],
                ),
            ],
        ),
        _modal(
            "Humanoid Robotics Control",
            "modal-3",
            "/assets/humanoids.png",
            "Synchronized humanoid robotics project",
            [
                _build_section_header("Technical implementation", "carbon:bot"),
                dmc.Stack(
                    gap=4,
                    children=[
                        _build_list_item("Multi-servo control for full-body articulation"),
                        _build_list_item("Custom gait and dance sequence programming in C"),
                        _build_list_item("Synchronized multi-robot performance"),
                    ],
                ),
                _build_section_header("Community impact", "carbon:group"),
                _body_text(
                    "Performances at Chung-Jung Church and Holt School for the Disabled used "
                    "robotics as a medium for entertainment and STEM education."
                ),
                _build_section_header("Outcomes", "carbon:result"),
                dmc.Stack(
                    gap=4,
                    children=[
                        _build_list_item("Demonstrated complex motor coordination"),
                        _build_list_item("Engaged diverse audiences with technology"),
                        _build_list_item("Connected engineering with performance"),
                    ],
                ),
            ],
        ),
    ]
