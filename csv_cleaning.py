import pandas as pd

# load the CSV
df = pd.read_csv("Anonymized-gift-history-PPL.csv")

# ensure all values are 5 digits with a leading zero if needed
df["Preferred ZIP"] = df["Preferred ZIP"].astype(str)
def format_zip(zip_code):
    if len(zip_code) < 5:
        return zip_code.zfill(5)  # add a leading zero
    else:
        return zip_code[:5]  # keep only the relevant digits
df["Preferred ZIP"] = df["Preferred ZIP"].apply(format_zip)
# print the updated column
print(df["Preferred ZIP"])

# generalize fund names
df["Fund Description"] = df["Fund Description"].astype(str)
# format to ignore the year of each specific fund and combine Annual Fund with PPL Annual Fund
def format_funds(fund_name):
    if fund_name == "PPL Annual Fund":
        return "Annual Fund"
    elif "Gala Event" in fund_name:
        return "Gala Event"
    elif "Savor the Story" in fund_name:
        return "Savor the Story"
    elif "Mysterium" in fund_name:
        return "Mysterium"
    elif "Think Again" in fund_name:
        return "Think Again Capital Campaign"
    else:
        return fund_name
df["Fund Description"] = df["Fund Description"].apply(format_funds)

# save back to CSV if needed
df.to_csv("updated_PPL_gift_history.csv", index=False)