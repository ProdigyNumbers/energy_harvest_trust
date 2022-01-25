# %%
import pandas as pd
import os

# %%
all_files = os.listdir("../data/output")
# %%
files = []
for file in all_files:
    if file.endswith(".csv"):
        files.append(file)
del all_files

# %%
full = pd.DataFrame()
for file in files:
    df = pd.read_csv(os.path.join("../data/output", file))
    df = df[["VH", "latitude", "longitude"]]
    date = file[17:25]
    df["date"] = pd.to_datetime(date)
    df['field'] = 'other'
    full = full.append(df)


# %%
full['date'].unique()

# %%
full.to_csv('../data/output_clean/other1.csv',index=False)

# %%

# %%
