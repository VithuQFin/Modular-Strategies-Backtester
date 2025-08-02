class Portfolio:
    def __init__(self, initial_cash, fee_rate=0.001):
        """
        Represents a simple long-only portfolio for backtesting.

        :param initial_cash: float - initial amount of cash
        :param fee_rate: float - transaction fee rate (default: 0.1%)
        """
        self.cash = initial_cash
        self.position = 0  # number of units held
        self.fee_rate = fee_rate
        self.history = []

    def buy(self, date, price):
        """
        Executes a buy order using all available cash.
        
        :param date: datetime - execution date
        :param price: float - asset price at execution
        :return: float - quantity purchased
        """
        quantity = (self.cash * (1 - self.fee_rate)) / price
        self.position += quantity
        self.cash = 0
        self.history.append((date, 'BUY', price, self.position, self.cash))
        return quantity

    def sell(self, date, price):
        """
        Executes a sell order for all held units.

        :param date: datetime - execution date
        :param price: float - asset price at execution
        :return: float - quantity sold
        """
        proceeds = self.position * price * (1 - self.fee_rate)
        quantity = self.position
        self.cash = proceeds
        self.position = 0
        self.history.append((date, 'SELL', price, self.position, self.cash))
        return quantity

    def update(self, date, price):
        """
        Logs the current state of the portfolio without any trade.

        :param date: datetime - current date
        :param price: float - current asset price
        """
        self.history.append((date, 'HOLD', price, self.position, self.cash))
