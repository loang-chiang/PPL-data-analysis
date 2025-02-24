import pandas as pd
import matplotlib.pyplot as plt
import textwrap

# import certifi
# import ssl
# import geopy.geocoders
# from geopy.exc import GeocoderTimedOut
# import time
# from geopy.geocoders import Nominatim

df = pd.read_csv("updated_PPL_gift_history.csv")

# zip codes with most donors - bar chart
df["Preferred ZIP"] = df["Preferred ZIP"].astype(str)
df = df[df["Preferred ZIP"].str.isnumeric()]  # keep only numeric ZIP codes
df_unique = df.drop_duplicates(subset=["Constituent ID"])  # delete duplicate donors
zip_counts = df_unique["Preferred ZIP"].value_counts()
top_donor_zip_codes = zip_counts.head(10)  # top ten zip codes with the most donors
zip_labels = [
    f"{zip_code}\n{df.loc[df['Preferred ZIP'] == zip_code, 'Location'].values[0]}"
    for zip_code in top_donor_zip_codes.index
]
plt.figure(figsize=(10, 6))
bars = plt.bar(zip_labels, top_donor_zip_codes.values, color="skyblue")

# labels and title
plt.xlabel("ZIP Code")
plt.ylabel("Number of Donors")
plt.title("Top 10 ZIP Codes with the Most Donors")
plt.xticks(rotation=90, ha="center", fontsize=10) 
plt.subplots_adjust(bottom=0.3)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()


# zip codes with the highest average gift amount - bar chart
# TODO: color
zip_avg_gift = df.groupby("Preferred ZIP")["Gift Amount"].mean()
df = df[df["Preferred ZIP"].str.isnumeric()]  # keep only numeric ZIP codes
top_gift_zip_codes = zip_avg_gift.sort_values(ascending=False).head(10)
zip_labels = [
    f"{zip_code}\n{df.loc[df['Preferred ZIP'] == zip_code, 'Location'].values[0]}"
    for zip_code in top_donor_zip_codes.index
]
plt.figure(figsize=(10, 6))
bars = plt.bar(zip_labels, top_gift_zip_codes.values, color="skyblue")
# labels and title
plt.xlabel("ZIP Code")
plt.ylabel("Gift Amount Mean")
plt.title("Top 10 ZIP Codes with the Highest Average Gift Amount")
plt.xticks(rotation=90, ha="center", fontsize=10) 
plt.subplots_adjust(bottom=0.3)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()


# TODO: donations to each fund
fund_counts = df_unique["Fund Description"].value_counts()
top_funds = fund_counts.nlargest(5)
others_total = fund_counts.iloc[5:].sum()

labels_and_sizes = top_funds.to_dict()
if others_total > 0:
    labels_and_sizes["Others"] = others_total

def wrap_labels(labels, width=15):
    return ['\n'.join(textwrap.wrap(label, width)) for label in labels]
wrapped_labels = wrap_labels(labels_and_sizes.keys())

fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(
    labels_and_sizes.values(),
    labels=wrapped_labels,
    autopct='%1.1f%%',
    textprops={"fontsize": 10},
    wedgeprops={"edgecolor": "white"},
)
plt.title("Top 5 Funds with the Highest Gift Amount", fontsize=14)
ax.legend(labels_and_sizes.keys(), title="Funds", loc="best", fontsize=10)
plt.axis("equal")
plt.show()


# TODO: funds with highest average gift amount
mean_per_fund = df_unique.groupby("Fund Description")["Gift Amount"].mean()
top_funds = mean_per_fund.sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
top_funds.plot(kind="bar", color="skyblue")
# labels and title
plt.xlabel("Fund Name")
plt.ylabel("Mean Gift Amount ")
plt.title("Top 10 Funds with the Highest Average Gift Amount")
plt.xticks(rotation=45, ha="right", fontsize=10) 
plt.subplots_adjust(bottom=0.3)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()


# TODO: top 10 biggest donors
df["Constituent ID"] = df["Constituent ID"].astype(str)
top_donors = df.groupby("Constituent ID")["Gift Amount"].sum().nlargest(10)
plt.bar(top_donors.index, top_donors.values, color="skyblue")

# labels and title
plt.figure(figsize=(12, 6))
plt.xlabel("Constituent ID")
plt.ylabel("Total Gift Amount")
plt.title("Top 10 Donors")
plt.xticks(rotation=90, ha="center", fontsize=10) 
plt.subplots_adjust(bottom=0.3)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()


# TODO: explore donors: history of top 20 donors
# get top 100
df["Gift Date"] = pd.to_datetime(df["Gift Date"])
df["Gift Amount"] = pd.to_numeric(df["Gift Amount"], errors="coerce")
top_donors = df.groupby("Constituent ID")["Gift Amount"].sum().nlargest(10).index
df_top = df[df["Constituent ID"].isin(top_donors)]
df_top_grouped = df_top.groupby(["Constituent ID", "Gift Date"])["Gift Amount"].sum().reset_index()
df_top_grouped = df_top_grouped.sort_values(["Constituent ID", "Gift Date"])

# plot donations over time
plt.figure(figsize=(12, 6))
for donor in df_top_grouped["Constituent ID"].unique():
    donor_data = df_top_grouped[df_top_grouped["Constituent ID"] == donor].copy()
    donor_data = donor_data.sort_values("Gift Date")
    plt.plot(donor_data["Gift Date"], donor_data["Gift Amount"], label=f"ID {donor}", alpha=0.7)

# labels and title
plt.xlabel("Date")
plt.ylabel("Gift Amount in Dollars")
plt.title("Donation Trends of Top 10 Donors")
plt.legend(fontsize=6, loc="upper left", bbox_to_anchor=(1, 1))
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()


# TODO: think again campaign



# # turn zip codes into locations
# ctx = ssl._create_unverified_context(cafile=certifi.where())
# geopy.geocoders.options.default_ssl_context = ctx
# geolocator = Nominatim(scheme='https', user_agent="Test")
# latitudes = []
# longitudes = []
# df_zip_unique = df.drop_duplicates(subset=["Preferred ZIP"])
# for zip_code in df_zip_unique["Preferred ZIP"]:
#     try:
#         location = geolocator.geocode(f"{zip_code}, USA", timeout=30)
#         if location:
#             latitudes.append(location.latitude)
#             longitudes.append(location.longitude)
#         else:
#             latitudes.append(None)
#             longitudes.append(None)
#         time.sleep(1)  # give the server some time
#     except GeocoderTimedOut:
#         print(f"Timeout for ZIP Code {zip_code}")
#         latitudes.append(None)
#         longitudes.append(None)

# # map lat and lon back to zip codes
# zip_to_lat_lon = dict(zip(df_zip_unique["Preferred ZIP"], zip(latitudes, longitudes)))
# df['lat'] = df['Preferred ZIP'].map(lambda x: zip_to_lat_lon.get(x, (None, None))[0])
# df['lon'] = df['Preferred ZIP'].map(lambda x: zip_to_lat_lon.get(x, (None, None))[1])