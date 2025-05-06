from fredapi import Fred
import pandas as pd

def fetch_yield_data(api_key, start="2005-01-01"):
    fred = Fred(api_key=api_key)
    tenors = ["DGS1","DGS2","DGS5","DGS10","DGS30"]
    df = fred.get_series_df(series=tenors, observation_start=start)
    df = df.rename(columns={"DGS1":"Y1","DGS2":"Y2","DGS5":"Y5","DGS10":"Y10","DGS30":"Y30"})
    return df.ffill()

if __name__ == "__main__":
    import os
    key = os.getenv("FRED_API_KEY")
    df = fetch_yield_data(key)
    df.to_csv("../data/raw/treasury_yields.csv")
