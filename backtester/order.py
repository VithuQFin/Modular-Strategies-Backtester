class Order:
    def __init__(self, date, order_type, price, quantity):
        """
        Represents an executed order in the backtest.

        :param date: datetime - execution date
        :param order_type: str - 'buy' or 'sell'
        :param price: float - asset price at execution
        :param quantity: float - quantity bought or sold
        """
        self.date = date
        self.order_type = order_type  # 'buy' or 'sell'
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f"[{self.date.date()}] {self.order_type.upper()} {self.quantity:.2f} @ {self.price:.2f}"

    def to_dict(self):
        return {
            "Date": self.date,
            "Type": self.order_type.upper(),
            "Price": self.price,
            "Quantity": self.quantity
        }
