# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams


plt.style.use("fivethirtyeight")
rcParams["axes.labelsize"] = 14
rcParams["xtick.labelsize"] = 12
rcParams["ytick.labelsize"] = 12
rcParams["figure.figsize"] = 16, 8
plt.style.use("seaborn-whitegrid")

# %%
# Other
other0 = pd.read_csv("../data/output_clean/other0.csv")
other1 = pd.read_csv("../data/output_clean/other1.csv")
other2 = pd.read_csv("../data/output_clean/other2.csv")

paddy0 = pd.read_csv("../data/output_clean/paddy0.csv")
paddy1 = pd.read_csv("../data/output_clean/paddy1.csv")
paddy2 = pd.read_csv("../data/output_clean/paddy2.csv")
paddy3 = pd.read_csv("../data/output_clean/paddy3.csv")
paddy4 = pd.read_csv("../data/output_clean/paddy4.csv")
paddy5 = pd.read_csv("../data/output_clean/paddy5.csv")
paddy6 = pd.read_csv("../data/output_clean/paddy6.csv")
paddy7 = pd.read_csv("../data/output_clean/paddy7.csv")
paddy8 = pd.read_csv("../data/output_clean/paddy8.csv")
paddy9 = pd.read_csv("../data/output_clean/paddy9.csv")
paddy10 = pd.read_csv("../data/output_clean/paddy10.csv")
paddy11 = pd.read_csv("../data/output_clean/paddy11.csv")
paddy12 = pd.read_csv("../data/output_clean/paddy12.csv")
paddy13 = pd.read_csv("../data/output_clean/paddy13.csv")
paddy14 = pd.read_csv("../data/output_clean/paddy14.csv")
paddy15 = pd.read_csv("../data/output_clean/paddy15.csv")
# %%
others_data = [other0, other1, other2]
paddy_data = [
    paddy0,
    paddy1,
    paddy2,
    paddy3,
    paddy4,
    paddy5,
    paddy6,
    paddy7,
    paddy8,
    paddy9,
    paddy10,
    paddy11,
    paddy12,
    paddy13,
    paddy14,
    paddy15,
]
# %%
for data in others_data:
    data["date"] = pd.to_datetime(data["date"].astype(str))
    print(data.shape)
for data in paddy_data:
    data["date"] = pd.to_datetime(data["date"].astype(str))
    print(data.shape)
# %%


# %%
plt.figure()
plt.title("Yearly horizontal backscatter evolution of fields with paddy and non-paddy")
# Other
for i, data in enumerate(others_data):
    if i == 0:
        plt.plot(data.groupby("date")["VH"].mean(), label="Other", color="b")
    else:
        plt.plot(data.groupby("date")["VH"].mean(), color="b")


# Paddy
for i, data in enumerate(paddy_data):
    if i == 0:
        plt.plot(data.groupby("date")["VH"].mean(), label="Paddy", color="r")
    else:
        plt.plot(data.groupby("date")["VH"].mean(), color="r")


plt.xticks(rotation=45)
plt.ylabel("VH Backscatter")
plt.legend()
plt.savefig("images/yearly.png")
plt.show()

# %%
other = pd.DataFrame()
for data in others_data:
    other = other.append(data)
paddy = pd.DataFrame()
for data in paddy_data:
    paddy = paddy.append(data)

# %%
plt.figure()
plt.title("Aggregated VH evolution of fields with paddy (15 fields) and non-paddy (3 fields)")
plt.plot(other.groupby("date")["VH"].mean(),label="Other", color="b")
plt.plot(paddy.groupby("date")["VH"].mean(),label="Paddy", color="r")
plt.xticks(rotation=45)
plt.ylabel("VH Backscatter")
plt.legend()
plt.savefig("images/yearly_aggregated.png")
plt.show()
# %%


# %%
