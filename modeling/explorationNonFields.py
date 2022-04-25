# %%
import pandas as pd
import os

# %%
non_field = pd.read_csv("../data/output_clean/non_fields.csv")
only_field = pd.read_csv("../data/output_clean/only_fields.csv")
# %%
non_field.day.unique()
# %%
only_field.month.unique()
# %%
full = pd.concat([non_field, only_field])
# %%
full.groupby("label").mean()
# %%
