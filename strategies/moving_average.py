class MovingAverageCrossStrategy:
    """
    Moving Average Crossover Strategy.
    Generates buy/sell signals based on the crossover between short and long moving averages.
    """

    def __init__(self, data, short_window, long_window):
        if short_window <= 0 or long_window <= 0:
            raise ValueError("Windows must be positive integers.")
        if short_window >= long_window:
            raise ValueError("short_window must be smaller than long_window.")
        if len(data) < long_window:
            raise ValueError("Data length is too short for the long window.")
        self.data = data.copy()
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self):
        df = self.data.copy()
        df['short_ma'] = df['Adj Close'].rolling(window=self.short_window).mean()
        df['long_ma'] = df['Adj Close'].rolling(window=self.long_window).mean()

        # Generate raw signal
        df['signal'] = 0
        df.loc[df['short_ma'] > df['long_ma'], 'signal'] = 1
        df.loc[df['short_ma'] < df['long_ma'], 'signal'] = -1

        # Shift signal to avoid lookahead bias
        df['signal'] = df['signal'].shift(1)
        return df
