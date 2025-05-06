import pandas as pd
import numpy as np

def backtest(df, entry_z=1.0, exit_z=0.0):
    df = df.copy()
    df["position"] = 0
    long = False
    for i in range(len(df)-1):
        if not long and df.S2_10_z.iloc[i] > entry_z:
            long = True
        elif long and df.S2_10_z.iloc[i] < exit_z:
            long = False
        df.position.iloc[i] = 1 if long else 0
    # daily PnL = position * ∆spread
    df["PnL"] = df.position.shift(1) * (df.S2_10.diff())
    df["cum_pnl"] = df.PnL.cumsum()
    return df

if __name__ == "__main__":
    df = pd.read_csv("../data/processed/features.csv", index_col=0, parse_dates=True)
    res = backtest(df)
    print("Sharpe:", res.PnL.mean() / res.PnL.std() * np.sqrt(252))
    res.cum_pnl.plot(title="Z-Score Backtest Equity")
