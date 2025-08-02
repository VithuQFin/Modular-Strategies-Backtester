class MeanReversionStrategy:
    """
    Mean Reversion Strategy based on z-score deviations of price from its moving average.
    Enters a long position when the price is significantly below the mean,
    and exits or shorts when the price is significantly above.
    """
    def __init__(self, data, window=20, threshold=1.0):
        if window <= 0:
            raise ValueError("Window size must be strictly positive.")
        self.data = data.copy()
        self.window = window
        self.threshold = threshold

    def generate_signals(self):
        df = self.data.copy()
        df['mean'] = df['Adj Close'].rolling(window=self.window).mean()
        df['std'] = df['Adj Close'].rolling(window=self.window).std()
        df['zscore'] = (df['Adj Close'] - df['mean']) / df['std']

        # Raw signal
        df['signal'] = 0
        df.loc[df['zscore'] < -self.threshold, 'signal'] = 1    # Buy signal (undervalued)
        df.loc[df['zscore'] > self.threshold, 'signal'] = -1    # Sell signal (overvalued)

        df['signal'] = df['signal'].shift(1)  # Avoid lookahead bias
        df['signal_change'] = df['signal'].diff()  # +2 or -2 on signal flip

        return df
