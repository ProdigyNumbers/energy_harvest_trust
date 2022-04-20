"""
This script cleans the output n output folder and moves it to output_clean
"""
# %%
import pandas as pd
import os

# %%
# Get the list of files in the output folder
non_fields = os.listdir("output/non_fields")

data = pd.DataFrame()
counter = 0
for field in non_fields:
    if field.endswith(".csv"):
        counter = counter + 1
        df = pd.read_csv("output/non_fields/" + field)
        year = non_fields[0].split("_")[5].split("T")[0][:4]
        month = non_fields[0].split("_")[5].split("T")[0][4:6]
        day = non_fields[0].split("_")[5].split("T")[0][6:8]
        df["year"] = year
        df["month"] = month
        df["day"] = day
        df["label"] = "non_field"
        df["counter"] = counter
        df = df.drop(columns=["system:index", ".geo"])
        data = data.append(df)

data.to_csv("output_clean/non_fields.csv", index=False)
# %%
only_fields = os.listdir("output/only_fields")

data = pd.DataFrame()
for field in only_fields:
    if field.endswith(".csv"):
        counter = counter + 1
        df = pd.read_csv("output/non_fields/" + field)
        year = non_fields[0].split("_")[5].split("T")[0][:4]
        month = non_fields[0].split("_")[5].split("T")[0][4:6]
        day = non_fields[0].split("_")[5].split("T")[0][6:8]
        df["year"] = year
        df["month"] = month
        df["day"] = day
        df["label"] = "only_field"
        df["counter"] = counter
        df = df.drop(columns=["system:index", ".geo"])
        data = data.append(df)

data.to_csv("output_clean/only_fields.csv", index=False)
