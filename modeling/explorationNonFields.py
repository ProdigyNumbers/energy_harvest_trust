# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from matplotlib import rcParams


plt.style.use("fivethirtyeight")
rcParams["axes.labelsize"] = 14
rcParams["xtick.labelsize"] = 12
rcParams["ytick.labelsize"] = 12
rcParams["figure.figsize"] = 16, 8
plt.style.use("seaborn-whitegrid")

non_field = pd.read_csv("../data/output_clean/non_fields.csv")
only_field = pd.read_csv("../data/output_clean/only_fields.csv")
only_field["label"] = "only_field"  ## TODO remov this when re-run the data cleaning
# %%
# Date treatment
non_field["date"] = (
    non_field["year"].astype(str)
    + "-"
    + non_field["month"].astype(str)
    + "-"
    + non_field["day"].astype(str)
)
non_field["date"] = pd.to_datetime(non_field["date"])
only_field["date"] = (
    only_field["year"].astype(str)
    + "-"
    + only_field["month"].astype(str)
    + "-"
    + only_field["day"].astype(str)
)
only_field["date"] = pd.to_datetime(only_field["date"])
# %%
df = pd.concat([non_field, only_field])
# %%
plt.figure()
plt.title("Yearly horizontal backscatter evolution of fields and non-fields")
plt.plot(only_field.groupby("date")["VH"].mean(), label="Fields", color="r")
plt.plot(non_field.groupby("date")["VH"].mean(), label="Non Fields", color="b")
plt.xticks(rotation=45)
plt.ylabel("VH Backscatter")
plt.legend()
plt.savefig("images/yearly_non_fields.png")
plt.show()
# %%
print("Number of Fields: " + str(only_field.counter.nunique()))
print("Number of Non Fields: " + str(non_field.counter.nunique()))
# %%
plt.figure()
plt.title(
    "Horizontal backscatter (10m pixel) distribution for July 2020 Field vs Non-Field"
)
sns.kdeplot(
    non_field[non_field["date"].dt.month == 7].VH.values, shade=True, label="Non Field"
)
sns.kdeplot(
    only_field[only_field["date"].dt.month == 7].VH.values,
    shade=True,
    label="Only Field",
)
plt.ylabel("VH Index")
plt.legend()
plt.savefig("images/pixelDensityPlotJulyNonFieldvsField.png")
plt.show()

# %%
plt.figure()
plt.title(
    "Horizontal backscatter (10m pixel) distribution for March 2020 Field vs Non-Field"
)
sns.kdeplot(
    non_field[non_field["date"].dt.month == 3].VH.values, shade=True, label="Non Field"
)
sns.kdeplot(
    only_field[only_field["date"].dt.month == 3].VH.values, shade=True, label="Field"
)
plt.ylabel("VH Index")
plt.legend()
plt.savefig("images/pixelDensityPlotMarchNonFieldvsField.png")
plt.show()
# %%
## Lets do a model
df["label"] = np.where(df["label"] == "only_field", 1, 0)
# %%

results = []
for val in df["month"].unique():
    X = df[df["month"] == val]
    X = X[["VH", "VV"]]
    y = df[df["month"] == val][["label"]]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, random_state=0, test_size=0.5, stratify=y
    )

    # dt = DecisionTreeClassifier(max_depth=3)
    model = Pipeline([("scaler", StandardScaler()), ("svc", LogisticRegression())])

    model.fit(X_train, y_train)

    res = model.predict_proba(X_test)[:, 1]

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
plt.savefig("images/thresholdMonthlyNonField.png")
plt.show()


# %%
X = df[df["month"] == 7]
X = X[["VH", "VV"]]
y = df[df["month"] == 7][["label"]]


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
data = df[df["month"] == 7]
data = data.sort_values("VH")
vals = set([int(i) for i in data["VH"].values])
# %%
prec = []
rec = []
aucs = []
perc = []
for val in vals:
    preds = np.where(data.VH < val, 1, 0)
    tn, fp, fn, tp = confusion_matrix(data["label"].values, preds).ravel()
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    aucs.append(roc_auc_score(data["label"].values, preds))
    prec.append(precision)
    rec.append(recall)

    perc.append(data[data.VH < val].shape[0] / data.shape[0])

# %%
plt.figure()
plt.title("Precision and Recall at different VH values for 7 Month Field/Non Field")
plt.plot(list(vals), prec, label="Precision")
plt.plot(list(vals), rec, label="Recall")
plt.plot(list(vals), aucs, label="AUC")
plt.plot(list(vals), perc, label="Percentage of data points")
plt.xlabel("VH Index")
plt.ylabel("Precision|Recall")
plt.legend()
plt.savefig("images/precisionRecallvariationNonField.png")
plt.show()

# %%
data[data.VH < val].shape[0]
# %%
only_field[(only_field.month == 2) & (only_field.day == 10)].shape
# %%
non_field[(non_field.month == 2) & (non_field.day == 10)].shape

# %%
