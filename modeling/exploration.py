# %%
import pandas as pd
import numpy as np
from rasterio import pad
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
paddy = pd.read_csv("data/output_clean/only_fields.csv")
non = pd.read_csv("data/output_clean/non_fields.csv")
cotton = pd.read_csv("data/output_clean/cotton_fields.csv")
# %%
# TODO THIS NEEDS TO BE FIXED -- Since we have enougth data, lets remove HH and HV without using the info
# cotton['VH'] = cotton['VH'].fillna(0) + cotton['HH'].fillna(0)
# cotton['VV'] = cotton['VV'].fillna(0) + cotton['HV'].fillna(0)
# cotton = cotton.drop(['HH', 'HV'], axis=1)
cotton = cotton.drop(["HH", "HV"], axis=1).dropna()
# %%
print("Paddy", paddy.counter.nunique())
print("Non field", non.counter.nunique())
print("Cotton", cotton.counter.nunique())
# %%
cotton.groupby(["counter", "month", "day"]).count()
# %%
k = []
for c in paddy.counter.unique():
    k.append(paddy[paddy.counter == c].shape[0])
n = []
for c in non.counter.unique():
    n.append(non[non.counter == c].shape[0])
e = []
for c in cotton.counter.unique():
    e.append(cotton[cotton.counter == c].shape[0])
sns.kdeplot(k)
sns.kdeplot(n)
sns.kdeplot(e)

# %%
plt.figure()
plt.title("Yearly horizontal backscatter evolution of fields with paddy, cotton and non-field")
plt.plot(paddy.groupby("month")["VH"].mean(), label="Paddy")
plt.plot(non.groupby("month")["VH"].mean(), label="Non Fields")
plt.plot(cotton.groupby("month")["VH"].mean(), label="Cotton")
plt.legend()
plt.savefig("modeling/images/yearlyVH.png")
plt.show()

# %%
plt.figure()
plt.title("Yearly horizontal backscatter evolution of fields with paddy and non-paddy")
plt.plot(paddy.groupby("month")["VV"].mean(), label="Paddy")
plt.plot(non.groupby("month")["VV"].mean(), label="Non Fields")
#plt.plot(cotton.groupby("month")["VV"].mean(), label="Cotton")
plt.legend()
plt.savefig("modeling/images/yearlyVV.png")
plt.show()
# %%

# %%

plt.figure()
plt.title("Horizontal backscatter (10m pixel) distribution for July 2020")
sns.kdeplot(non[non["month"] == 7].VH.values, shade=True, label="Other")
sns.kdeplot(paddy[paddy["month"] == 7].VH.values, shade=True, label="Paddy")
sns.kdeplot(cotton[cotton["month"] == 7].VH.values, shade=True, label="Cotton")
plt.ylabel("VH Index")
plt.legend()
plt.savefig("modeling/images/pixelDensityPlotJuly.png")
plt.show()

# %%
plt.figure()
plt.title("Horizontal backscatter (10m pixel) distribution for March 2020")
sns.kdeplot(non[non["month"] == 3].VH.values, shade=True, label="Other")
sns.kdeplot(paddy[paddy["month"] == 3].VH.values, shade=True, label="Paddy")
sns.kdeplot(cotton[cotton["month"] == 3].VH.values, shade=True, label="Cotton")
plt.ylabel("VH Index")
plt.legend()
plt.savefig("modeling/images/pixelDensityPlotMarch.png")
plt.show()
# %%

# %%
