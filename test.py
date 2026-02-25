print("STARTED")

import pandas as pd

df = pd.read_csv("data/sales_data.csv", encoding="latin1")

print(df.head())
print("\nTotal Sales:", df["Sales"].sum())

print("DONE")