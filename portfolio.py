import pandas as pd
from datetime import datetime

class Portfolio:
    def __init__(self, starting_balance: float):
        self.balance = starting_balance
        self.holdings = {}  # {coin, quantity and average price}
        self.transaction_history = []

    #transaction

    def validate_transaction(self, crypto: str, quantity: float, price: float, transaction_type: str) -> bool:
        if quantity <= 0 or price <= 0:
            return False

        if transaction_type == "buy":
            return self.balance >= quantity * price

        if transaction_type == "sell":
            return crypto in self.holdings and self.holdings[crypto]["quantity"] >= quantity

        return False

    # buy cryptocurrency
   
    def buy_crypto(self, crypto: str, quantity: float, price: float):
        if not self.validate_transaction(crypto, quantity, price, "buy"):
            raise ValueError("Invalid buy transaction")

        cost = quantity * price
        self.balance -= cost

        if crypto in self.holdings:
            old_qty = self.holdings[crypto]["quantity"]
            old_price = self.holdings[crypto]["avg_price"]

            new_qty = old_qty + quantity
            new_avg_price = ((old_qty * old_price) + (quantity * price)) / new_qty

            self.holdings[crypto]["quantity"] = new_qty
            self.holdings[crypto]["avg_price"] = new_avg_price
        else:
            self.holdings[crypto] = {
                "quantity": quantity,
                "avg_price": price
            }

        self._log_transaction("BUY", crypto, quantity, price)

    # sell cryptocurrency

    def sell_crypto(self, crypto: str, quantity: float, price: float):
        if not self.validate_transaction(crypto, quantity, price, "sell"):
            raise ValueError("Invalid sell transaction")

        self.balance += quantity * price
        self.holdings[crypto]["quantity"] -= quantity

        if self.holdings[crypto]["quantity"] == 0:
            del self.holdings[crypto]

        self._log_transaction("SELL", crypto, quantity, price)

  
    def display_portfolio(self, current_prices: dict):
        print("\n USER PORTFOLIO DASHBOARD")
        print("-" * 40)
        print(f"Available Balance: ${self.balance:.2f}\n")

        for crypto, data in self.holdings.items():
            current_price = current_prices.get(crypto, 0)
            invested = data["quantity"] * data["avg_price"]
            current_value = data["quantity"] * current_price
            profit_loss = current_value - invested

            print(f"{crypto}")
            print(f"  Quantity: {data['quantity']}")
            print(f"  Avg Buy Price: ${data['avg_price']:.2f}")
            print(f"  Current Price: ${current_price:.2f}")
            print(f"  P/L: ${profit_loss:.2f}\n")


    def portfolio_value(self, current_prices: dict) -> float:
        total_value = self.balance

        for crypto, data in self.holdings.items():
            total_value += data["quantity"] * current_prices.get(crypto, 0)

        return total_value

 
    def pd_array(self, historical_data: list):
        """
        historical_data = [
            {"date": "2024-01-01", "price": 43000},
            {"date": "2024-01-02", "price": 43500}
        ]
        """
        df = pd.DataFrame(historical_data)
        df["date"] = pd.to_datetime(df["date"])
        return df.values

    # internal: transaction logger
   
    def _log_transaction(self, t_type, crypto, quantity, price):
        self.transaction_history.append({
            "type": t_type,
            "crypto": crypto,
            "quantity": quantity,
            "price": price,
            "timestamp": datetime.now()
        })
