import pandas as pd

# load the CSV
df = pd.read_csv("Anonymized-gift-history-PPL.csv", dtype={"Preferred ZIP": str})
df["Preferred ZIP"] = df["Preferred ZIP"].astype(str)

# ensure all values are 5 digits with a leading zero if needed
def format_zip(zip_code):
    if len(zip_code) < 5:
        return zip_code.zfill(5)  # add a leading zero
    else:
        return zip_code[:5]  # keep only the relevant digits
df["Preferred ZIP"] = df["Preferred ZIP"].apply(format_zip)

# print the updated column
print(df["Preferred ZIP"])

# save back to CSV if needed
df.to_csv("updated_PPL_gift_history.csv", index=False)