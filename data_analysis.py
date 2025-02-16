import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("updated_PPL_gift_history.csv")
df["Preferred ZIP"] = df["Preferred ZIP"].astype(str)

# zip codes with most donors
df_unique = df.drop_duplicates(subset=["Constituent ID"])  # delete duplicate donors
zip_counts = df_unique["Preferred ZIP"].value_counts()
top_zip_codes = zip_counts.head(10)  # top ten zip codes with the most donors
plt.figure(figsize=(10, 6))
top_zip_codes.plot(kind="bar", color="skyblue")

# labels and title
plt.xlabel("ZIP Code")
plt.ylabel("Number of Donors")
plt.title("Top 10 ZIP Codes with the Most Donors")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()