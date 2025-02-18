import pandas as pd
import matplotlib.pyplot as plt

import certifi
import ssl
import geopy.geocoders
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
import geopandas as gpd
from shapely.geometry import Point

df = pd.read_csv("updated_PPL_gift_history.csv")
df["Preferred ZIP"] = df["Preferred ZIP"].astype(str)

# zip codes with most donors - bar chart
df_unique = df.drop_duplicates(subset=["Constituent ID"])  # delete duplicate donors
zip_counts = df_unique["Preferred ZIP"].value_counts()
top_donor_zip_codes = zip_counts.head(10)  # top ten zip codes with the most donors
plt.figure(figsize=(10, 6))
top_donor_zip_codes.plot(kind="bar", color="skyblue")
# labels and title
plt.xlabel("ZIP Code")
plt.ylabel("Number of Donors")
plt.title("Top 10 ZIP Codes with the Most Donors")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

# zip codes with the highest average gift amount - bar chart
zip_avg_gift = df.groupby("Preferred ZIP")["Gift Amount"].mean()
top_gift_zip_codes = zip_avg_gift.sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
top_gift_zip_codes.plot(kind="bar", color="skyblue")
# labels and title
plt.xlabel("ZIP Code")
plt.ylabel("Gift Amount Mean")
plt.title("Top 10 ZIP Codes with the Highest Average Gift Amount")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

# correlation between zip code and funds donated to - map
ctx = ssl._create_unverified_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx
geolocator = Nominatim(scheme='https', user_agent="Test")
latitudes = []
longitudes = []
for zip_code in df["Preferred ZIP"]:
    try:
        location = geolocator.geocode(f"{zip_code}, USA")
        if location:
            latitudes.append(location.latitude)
            longitudes.append(location.longitude)
        else:
            latitudes.append(None)
            longitudes.append(None)
    except GeocoderTimedOut:
        print(f"Timeout for ZIP Code {zip_code}")
        latitudes.append(None)
        longitudes.append(None)

# add lat and lon to the df
df['lat'] = latitudes
df['lon'] = longitudes

geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
geo_df = gpd.GeoDataFrame(df, geometry=geometry)
geo_df.plot(marker='o', color='red', markersize=5)
plt.title("Geospatial Distribution of Donations by ZIP Code")
plt.show()