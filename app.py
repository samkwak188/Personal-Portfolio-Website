from dash import Dash

from portfolio_app import build_layout, register_callbacks


app = Dash(
    __name__,
    title="Changyong Kwak | Software Engineer",
    update_title=None,
    external_stylesheets=[
        (
            "https://fonts.googleapis.com/css2?"
            "family=Instrument+Sans:wdth,wght@75..100,400..700&"
            "family=Source+Sans+3:wght@400;500;600&display=swap"
        )
    ],
    meta_tags=[
        {
            "name": "description",
            "content": (
                "Changyong Kwak is a UW-Madison computer science student building "
                "robotics controls, test infrastructure, and developer systems."
            ),
        },
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "theme-color", "content": "#0b0c0c"},
        {"property": "og:title", "content": "Changyong Kwak | Software Engineer"},
        {
            "property": "og:description",
            "content": "Software, research, robotics, and product work by Changyong Kwak.",
        },
    ],
)
app.config.suppress_callback_exceptions = True
server = app.server

app.layout = build_layout()
register_callbacks(app)


if __name__ == "__main__":
    app.run(debug=False)

