import dash
from dash import dcc, html
import plotly.express as px

from data import (
    user_portfolio,
    market_summary,
    historical_prices,
    selected_crypto,
    selected_timeframe,
    notif_array
)
from predictions import predict_prices

# load data
market = market_summary()
prices = historical_prices(selected_crypto.lower(), selected_timeframe)
prices = predict_prices(prices)

# dashboard graphs
def dashboard_graphs():
    fig = px.line(
        prices,
        x="timestamp",
        y=["price", "predicted"],
        title=f"{selected_crypto} Actual vs Predicted Price"
    )
    return fig


# app setup
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Crypto Prediction Dashboard"),

    html.Div([
        html.H3("🌍 Market Summary"),
        html.P(f"Total Market Cap: ${market['market_cap']:,.0f}"),
        html.P(f"24h Volume: ${market['volume']:,.0f}"),
        html.P(f"BTC Dominance: {market['btc_dominance']:.2f}%")
    ]),

    html.Div([
        html.H3("User Portfolio"),
        html.Ul([
            html.Li(f"{coin['symbol']}: {coin['amount']} coins")
            for coin in user_portfolio
        ])
    ]),

    html.Div([
        html.H3("Price Charts"),
        dcc.Graph(figure=dashboard_graphs())
    ]),

    html.Div([
        html.H3("Notifications"),
        html.Ul([
            html.Li(alert) for alert in notif_array
        ])
    ])
])


if __name__ == "__main__":
    app.run_server(debug=True)
