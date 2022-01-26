# %%
import pandas as pd
import numpy as np
import seaborn as sns

sns.set_theme(style="whitegrid")
import matplotlib.pyplot as plt
from matplotlib import rcParams
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix
from sklearn.model_selection import train_test_split

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
other3 = pd.read_csv("../data/output_clean/other3.csv")
other4 = pd.read_csv("../data/output_clean/other4.csv")
other5 = pd.read_csv("../data/output_clean/other5.csv")
other6 = pd.read_csv("../data/output_clean/other6.csv")
other7 = pd.read_csv("../data/output_clean/other7.csv")
other8 = pd.read_csv("../data/output_clean/other8.csv")
other9 = pd.read_csv("../data/output_clean/other9.csv")
other10 = pd.read_csv("../data/output_clean/other10.csv")
other11 = pd.read_csv("../data/output_clean/other11.csv")
other12 = pd.read_csv("../data/output_clean/other12.csv")
other13 = pd.read_csv("../data/output_clean/other13.csv")
other14 = pd.read_csv("../data/output_clean/other14.csv")
other15 = pd.read_csv("../data/output_clean/other15.csv")

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
others_data = [
    other0,
    other1,
    other2,
    other3,
    other4,
    other5,
    other6,
    other7,
    other8,
    other9,
    other10,
    other11,
    other12,
    other13,
    other14,
    other15,
]
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
    data["paddy"] = 0
    print(data.shape)
for data in paddy_data:
    data["date"] = pd.to_datetime(data["date"].astype(str))
    print(data.shape)
    data["paddy"] = 1

# %%
df = pd.DataFrame()
for data in others_data:
    df = df.append(data)

for data in paddy_data:
    df = df.append(data)

# %%
results = []
for val in df["date"].dt.month.unique():
    print(val)
    X = df[df["date"].dt.month == val].drop(
        columns=["date", "field", "latitude", "longitude", "paddy"]
    )
    y = df[df["date"].dt.month == val][["paddy"]]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, random_state=0, test_size=0.5, stratify=y
    )

    # dt = DecisionTreeClassifier(max_depth=3)
    dt = LogisticRegression()
    dt.fit(X_train, y_train)

    res = dt.predict_proba(X_test)[:, 1]

    results.append([val, roc_auc_score(y_test, res)])

results = pd.DataFrame(results, columns=["date", "score"])

# %%
plt.figure()
plt.title("Monthly classification performance throughout 2020")
plt.ylim([0.4, 1])
sns.barplot(results["date"], results.score, palette="Blues_d")
plt.ylabel("AUC")
plt.xlabel("Months of 2020")
plt.xticks(rotation=45)
plt.savefig("images/thresholdMonthly.png")
plt.show()


# %%
X = df[df["date"].dt.month == 7].drop(
    columns=["date", "field", "latitude", "longitude", "paddy"]
)
y = df[df["date"].dt.month == 7][["paddy"]]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, random_state=0, test_size=0.5, stratify=y
)

dt = LogisticRegression()
dt.fit(X_train, y_train)
# %%
roc_auc_score(y_test, dt.predict_proba(X_test)[:, 1])

# %%
tn, fp, fn, tp = confusion_matrix(dt.predict(X_test), y_test).ravel()
# %%
# Precision
tp / (tp + fp)
# %%
# Accuracy
tp / (tp + fn)
# %%
# F1
tp / (tp + 0.5 * (fp + fn))

# %%
data = df[df["date"].dt.month == 7]
data = data.sort_values("VH")
vals = set([int(i) for i in data["VH"].values])
# %%
prec = []
rec = []
aucs = []
perc = []
for val in vals:
    preds = np.where(data.VH < val, 1, 0)
    tn, fp, fn, tp = confusion_matrix(data["paddy"].values, preds).ravel()
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    aucs.append(roc_auc_score(data["paddy"].values, preds))
    prec.append(precision)
    rec.append(recall)

    perc.append(data[data.VH < val].shape[0] / data.shape[0])

# %%
plt.figure()
plt.title("Precision and Recall at different VH values for 7 Month")
plt.plot(list(vals), prec, label="Precision")
plt.plot(list(vals), rec, label="Recall")
plt.plot(list(vals), aucs, label="AUC")
plt.plot(list(vals), perc, label="Percentage of data points")
plt.xlabel("VH Index")
plt.ylabel("Precision|Recall")
plt.legend()
plt.savefig("images/precisionRecallvariation.png")
plt.show()

# %%
data[data.VH < val].shape[0]
# %%
