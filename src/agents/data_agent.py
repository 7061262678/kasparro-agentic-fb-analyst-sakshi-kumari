import pandas as pd
from src.utils.data_loader import load_csv

class DataAgent:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def load_and_aggregate(self):
        df = load_csv(self.config["data"]["path"], self.config["data"]["date_column"])
        df.sort_values(self.config["data"]["date_column"], inplace=True)

        df["roas"] = df["revenue"] / df["spend"].replace(0, pd.NA)
        df["ctr"] = df["clicks"] / df["impressions"].replace(0, pd.NA)
        df["cvr"] = df["purchases"] / df["clicks"].replace(0, pd.NA)

        daily = df.groupby(self.config["data"]["date_column"]).agg(
            spend=("spend", "sum"),
            revenue=("revenue", "sum"),
            ctr=("ctr", "mean"),
            cvr=("cvr", "mean"),
            roas=("roas", "mean")
        ).reset_index()

        self.logger.log("loaded_data", {"rows": int(df.shape[0])})
        return {"raw": df, "daily": daily}
