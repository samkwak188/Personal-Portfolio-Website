from dash import Dash

from portfolio_app import build_layout, register_callbacks


app = Dash(
    __name__,
    title="Changyong Kwak | Software Engineer",
    meta_tags=[
        {
            "name": "description",
            "content": (
                "Changyong Kwak is a UW-Madison computer science student building "
                "robotics controls, test infrastructure, and developer systems."
            ),
        },
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"property": "og:title", "content": "Changyong Kwak | Software Engineer"},
        {
            "property": "og:description",
            "content": "Selected work across robotics controls, AI evaluation, and developer tools.",
        },
    ],
)
app.config.suppress_callback_exceptions = True
server = app.server

app.layout = build_layout()
register_callbacks(app)


if __name__ == "__main__":
    app.run(debug=False)

