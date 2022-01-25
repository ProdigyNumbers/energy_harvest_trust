# %%
import pandas as pd
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
paddy0 = pd.read_csv("../data/output_clean/paddy0.csv")
paddy1 = pd.read_csv("../data/output_clean/paddy1.csv")
# %%
other0["date"] = pd.to_datetime(other0["date"].astype(str))
other1["date"] = pd.to_datetime(other1["date"].astype(str))
paddy0["date"] = pd.to_datetime(paddy0["date"].astype(str))
paddy1["date"] = pd.to_datetime(paddy1["date"].astype(str))

# %%
plt.figure()
plt.title("Yearly horizontal backscatter evolution of fields with paddy and non-paddy")
# Other
plt.plot(other0.groupby("date")["VH"].mean(), label="Other", color="b")
plt.plot(other1.groupby("date")["VH"].mean(), color="b")

# Paddy
plt.plot(paddy0.groupby("date")["VH"].mean(), label="Paddy", color="r")
plt.plot(paddy1.groupby("date")["VH"].mean(), color="r")
plt.xticks(rotation=45)
plt.ylabel("VH Backscatter")
plt.legend()
plt.savefig("images/yearly.png")
plt.show()

# %%
sorted(other1["date"].unique())
# %%
