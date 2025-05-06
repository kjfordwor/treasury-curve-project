import pandas as pd

def engineer_features(df):
    # Spreads
    df["S2_10"] = df.Y10 - df.Y2
    df["S5_30"] = df.Y30 - df.Y5
    # Rolling stats
    w = 60
    df["S2_10_mean"] = df.S2_10.rolling(w).mean()
    df["S2_10_std"]  = df.S2_10.rolling(w).std()
    df["S2_10_z"]    = (df.S2_10 - df.S2_10_mean) / df.S2_10_std
    # EWMA vol
    df["Y10_vol"] = df.Y10.ewm(halflife=21).std()
    # Carry & Label
    df["S2_10_next"]    = df.S2_10.shift(-21)
    df["Carry_2_10"]    = df.S2_10_next - df.S2_10
    df["Label_flatten"] = (df.S2_10_next < df.S2_10).astype(int)
    return df.dropna()

if __name__ == "__main__":
    df = pd.read_csv("../data/raw/treasury_yields.csv", index_col=0, parse_dates=True)
    df_feat = engineer_features(df)
    df_feat.to_csv("../data/processed/features.csv")
