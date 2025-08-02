from backtester.order import Order
from backtester.portfolio import Portfolio

class BacktestEngine:
    def __init__(self, strategy, data, initial_cash=100000, fee_rate=0.001):
        self.strategy = strategy
        self.data = data
        self.portfolio = Portfolio(initial_cash, fee_rate=fee_rate)
        self.orders = []

    def run(self):
        df = self.strategy.generate_signals()

        for i in range(len(df)):
            row = df.iloc[i]
            signal = row['signal']
            date = row['Date']
            price = row['Adj Close']

            if signal > 0 and self.portfolio.cash > 0:
                quantity = self.portfolio.buy(date, price)
                self.orders.append(Order(date, 'buy', price, quantity))

            elif signal < 0 and self.portfolio.position > 0:
                quantity = self.portfolio.sell(date, price)
                self.orders.append(Order(date, 'sell', price, quantity))

            else:
                self.portfolio.update(date, price)

        return df
