"""Styling primitives shared across the portfolio Dash application."""

CARD_STYLE = {
    "width": "100%",
    "minHeight": 380,
    "height": "100%",
    "display": "flex",
    "flexDirection": "column",
    "backgroundColor": "transparent", 
    "border": "none",
}

TAB_BUTTON_STYLE = {
    "fontSize": "15px",
    "fontWeight": 500,
}

PAGE_WRAPPER_STYLE = {
    "backgroundColor": "#050505",
    "minHeight": "100vh",
    "color": "#e2e8f0",
    "fontFamily": "'Inter', sans-serif",
    "overflowX": "hidden",
    # Complex mesh gradient background
    "backgroundImage": """
        radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(168, 85, 247, 0.15) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.1) 0px, transparent 50%),
        radial-gradient(at 0% 100%, rgba(34, 211, 238, 0.1) 0px, transparent 50%)
    """,
    "backgroundAttachment": "fixed",
}

MANTINE_THEME = {
    "colorScheme": "dark",
    "primaryColor": "violet",
    "fontFamily": "'Inter', sans-serif",
    "defaultRadius": "md",
    "components": {
        "Card": {
            "styles": {
                "root": {
                    "backgroundColor": "transparent",
                }
            }
        },
        "Button": {
            "styles": {
                "root": {
                    "transition": "transform 0.1s ease, box-shadow 0.2s ease",
                    "&:hover": {
                        "transform": "translateY(-1px)",
                        "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.2)",
                    },
                    "&:active": {
                        "transform": "translateY(0)",
                    }
                }
            }
        },
        "Badge": {
            "styles": {
                "root": {
                    "textTransform": "uppercase",
                    "letterSpacing": "0.5px",
                    "fontWeight": 700,
                }
            }
        }
    },
}
