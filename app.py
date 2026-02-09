from dash import Dash

from portfolio_app import build_layout, register_callbacks


app = Dash(__name__, title="Sam Kwak - Portfolio")
app.config.suppress_callback_exceptions = True
server = app.server

app.layout = build_layout()
register_callbacks(app)


if __name__ == "__main__":
    app.run(debug=False)

