import requests
import pandas as pd

# variables
selected_crypto = "BTC"
selected_timeframe = 30  # days

# -------- Arrays --------
user_portfolio = [
    {"symbol": "BTC", "amount": 0.5, "current_value": 0},
    {"symbol": "ETH", "amount": 2, "current_value": 0},
]

notif_array = []


# procedures
def market_summary():
    """
    Shows the summary of the market
    """
    url = "https://api.coingecko.com/api/v3/global"
    data = requests.get(url).json()["data"]

    return {
        "market_cap": data["total_market_cap"]["gbp"],
        "volume": data["total_volume"]["gbp"],
        "btc_dominance": data["market_cap_percentage"]["btc"]
    }


def historical_prices(symbol, days):
    """
    Downloads historical price data for cryptocurrencies
    """
    url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart"
    params = {"vs_currency": "gbp", "days": days}

    data = requests.get(url, params=params).json()
    prices = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    prices["timestamp"] = pd.to_datetime(prices["timestamp"], unit="ms")

    return prices
