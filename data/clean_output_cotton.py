"""
This script cleans the output n output folder and moves it to output_clean
"""
# %%
import pandas as pd
import os

# %%
# Get the list of files in the output folder
non_fields = os.listdir("output/gdrive/8_May_2022/Cotton_Mansa_Region")
data = pd.DataFrame()
counter = 0
for field in non_fields:
    field_path = os.path.join("output/gdrive/8_May_2022/Cotton_Mansa_Region", field)
    field_files = os.listdir(field_path)
    counter = counter + 1
    for file in field_files:
        if file.endswith(".csv"):
            # Check if file to read is empty
            try:
                df = pd.read_csv(os.path.join(field_path, file))
            except pd.errors.EmptyDataError:
                # print('Note: {} was empty. Skipping.'.format(os.path.join(field_path , file)))
                continue  # will skip the rest of the block and move to next file
            year = file.split("_")[5].split("T")[0][:4]
            month = file.split("_")[5].split("T")[0][4:6]
            day = file.split("_")[5].split("T")[0][6:8]
            df["year"] = year
            df["month"] = month
            df["day"] = day
            df["label"] = "cotton"
            df["counter"] = counter
            df = df.drop(columns=["system:index", ".geo"])
            data = data.append(df)

print("Non field shape is: ", data.shape)
data.to_csv("output_clean/cotton_fields.csv", index=False)
