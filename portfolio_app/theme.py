"""Styling primitives shared across the portfolio Dash application."""

CARD_STYLE = {
    "width": "100%",
    "minHeight": 420,
    "height": "100%",
    "display": "flex",
    "flexDirection": "column",
    "backgroundColor": "rgba(30, 41, 59, 0.3)",  # Darker, tailored background
    "border": "1px solid rgba(255, 255, 255, 0.08)",
}

TAB_BUTTON_STYLE = {
    "fontSize": "15px",
    "fontWeight": 500,
}

PAGE_WRAPPER_STYLE = {
    "backgroundColor": "#050505",  # Deep black/blue
    "minHeight": "100vh",
    "color": "#e2e8f0",
    "fontFamily": "'Inter', sans-serif",
    "overflowX": "hidden",
    "backgroundImage": "radial-gradient(circle at 15% 50%, rgba(99, 102, 241, 0.08), transparent 25%), radial-gradient(circle at 85% 30%, rgba(168, 85, 247, 0.08), transparent 25%)",
}

MANTINE_THEME = {
    "colorScheme": "dark",
    "primaryColor": "violet",
    "fontFamily": "'Inter', sans-serif",
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
                    "transition": "transform 0.1s ease",
                }
            }
        }
    },
}
