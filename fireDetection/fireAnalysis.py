# %%
import pandas as pd
import folium


# %%
firms = pd.read_excel("../data/punjab_september_2020.xlsx")

# %%

firms["acq_date"] = pd.to_datetime(firms["acq_date"])
# %%

# %%
m = folium.Map(location=[30.54450917853599, 76.61544614399376])


# %%
folium.Circle(
    radius=100,
    location=[45.5244, -122.6699],
    popup="The Waterfront",
    color="crimson",
    fill=False,
).add_to(m)

# %%
for index, row in df.iterrows():

    folium.Circle(
            radius=100,
            location=[row["latitude"], row["longitude"]],
            color="crimson",
            fill=False,
        ).add_to(m)
# %%
m
# %%
