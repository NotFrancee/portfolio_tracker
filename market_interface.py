import os
import yfinance as yf
import pandas as pd
from alpha_vantage.timeseries import TimeSeries


class MarketInterface:
    """Util class for basic functions"""

    def __init__(self):
        self.alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

        if self.alpha_vantage_api_key is None:
            raise Exception(
                "The Alpha Vantage API Key was not found. Make sure there is a .env file in the folder, with an env var named <alpha_vantage_api_key>"
            )

        self.ts = TimeSeries(
            key=self.alpha_vantage_api_key, output_format="pandas"
        )

    def get_stocks_prices(self, tickers: list[str], start="2000-1-1"):
        """Loads stock prices for multiple tickers from YFinance

        Args:
            tickers (list[str])
            start (str, optional): start date for the data.
            Defaults to "2000-1-1".

        Returns:
            pd.DataFrame
        """

        d = dict()

        print("\tretrieving prices:", end=" ")

        for ticker in tickers:
            print(ticker, end=" ")

            t_data = yf.Ticker(ticker)

            hist_prices = t_data.history(start=start, interval="1d")

            shares = t_data.get_shares_full(start=start)
            shares = shares[~(shares.index.duplicated())]
            shares = shares.reindex(hist_prices.index, fill_value=float("NaN"))
            shares = shares.fillna(method="ffill")

            # change columns
            new_columns = {col: col.lower() for col in hist_prices.columns}
            hist_prices.rename(columns=new_columns, inplace=True)

            hist_prices["daily_return"] = hist_prices["close"].pct_change(1)
            hist_prices["vol_1mo"] = (
                hist_prices["daily_return"].rolling(21).std()
            )
            hist_prices["vol_3mo"] = (
                hist_prices["daily_return"].rolling(63).std()
            )
            hist_prices["vol_12mo"] = (
                hist_prices["daily_return"].rolling(252).std()
            )
            hist_prices["market_cap"] = shares * hist_prices["close"]

            d[ticker] = hist_prices

        # you have to pull the historical composition
        # of FTSEMIB and calc returns on that
        df = pd.concat(d.values(), axis=1, keys=d.keys())
        print("-> retrieved all prices")
        return df
