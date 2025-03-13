import pandas as pd
import matplotlib.pyplot as plt
import textwrap
import matplotlib.cm as cm
import matplotlib.ticker as mtick
import seaborn as sns  # for color palette

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

# unique bar color for each city
zip_locations = df_unique.set_index("Preferred ZIP")["Location"].to_dict()
unique_cities = sorted(list(set(zip_locations.values())))
palette = sns.color_palette("husl", len(unique_cities))
city_colors = dict(zip(unique_cities, palette))
bar_colors = [city_colors[zip_locations[zip_code]] for zip_code in top_donor_zip_codes.index]
bars = plt.bar(zip_labels, top_donor_zip_codes.values, color=bar_colors)

# labels and title
plt.xlabel("ZIP Code")
plt.ylabel("Number of Donors")
plt.title("Top 10 ZIP Codes with the Most Donors")
plt.xticks(rotation=90, ha="center", fontsize=10) 
plt.subplots_adjust(bottom=0.3)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()


# zip codes with the highest average gift amount - bar chart
zip_avg_gift = df.groupby("Preferred ZIP")["Gift Amount"].mean()
df = df[df["Preferred ZIP"].str.isnumeric()]  # keep only numeric ZIP codes
top_gift_zip_codes = zip_avg_gift.sort_values(ascending=False).head(10)
zip_labels = [
    f"{zip_code}\n{df.loc[df['Preferred ZIP'] == zip_code, 'Location'].values[0]}"
    for zip_code in top_gift_zip_codes.index
]
plt.figure(figsize=(10, 6))

# unique bar color for each city
zip_locations = df_unique.set_index("Preferred ZIP")["Location"].to_dict()
unique_cities = sorted(list(set(zip_locations.values())))
city_colors = dict(zip(unique_cities, palette))
bar_colors = [city_colors[zip_locations[zip_code]] for zip_code in top_gift_zip_codes.index]
bars = plt.bar(zip_labels, top_gift_zip_codes.values, color=bar_colors)

# labels and title
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.xlabel("ZIP Code")
plt.ylabel("Gift Amount Mean")
plt.title("Top 10 ZIP Codes with the Highest Average Gift Amount")
plt.xticks(rotation=90, ha="center", fontsize=10) 
plt.subplots_adjust(bottom=0.3)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()


# donations to each fund
fund_counts = df_unique["Fund Description"].value_counts()
top_funds = fund_counts.nlargest(6)
others_total = fund_counts.iloc[6:].sum()

labels_and_sizes = top_funds.to_dict()
if others_total > 0:
    labels_and_sizes["Others"] = others_total

def wrap_labels(labels, width=15):
    return ['\n'.join(textwrap.wrap(label, width)) for label in labels]
wrapped_labels = wrap_labels(labels_and_sizes.keys())

# labels and title
fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    labels_and_sizes.values(),
    labels=wrapped_labels,
    autopct='%1.1f%%',
    textprops={"fontsize": 10},
    wedgeprops={"edgecolor": "white"},
    labeldistance=1.1,
)
for text in texts:
    if text.get_text() == wrap_labels(["Annual Fund"])[0]:
        text.set_y(text.get_position()[1] - 0.5)  # move label down
        text.set_x(text.get_position()[0] - 0.8)  # move label left
        text.set_horizontalalignment("right")
plt.title("Top 5 Funds with the Highest Gift Amount", fontsize=14)
ax.legend(labels_and_sizes.keys(), title="Funds", loc="best", fontsize=10)
plt.axis("equal")
plt.show()


# funds with highest average gift amount
mean_per_fund = df_unique.groupby("Fund Description")["Gift Amount"].mean()
top_funds = mean_per_fund.sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x:,.0f}"))
top_funds.plot(kind="bar", color="mediumseagreen")

# labels and title
plt.xlabel("Fund Name")
plt.ylabel("Mean Gift Amount ")
plt.title("Top 10 Funds with the Highest Average Gift Amount")
plt.xticks(rotation=45, ha="right", fontsize=10) 
plt.subplots_adjust(bottom=0.3)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()


# funds with highest average gift amount (leave out major gifts)
mean_per_fund = df_unique.groupby("Fund Description")["Gift Amount"].mean()
top_funds = mean_per_fund.sort_values(ascending=False).head(11)[1:]
plt.figure(figsize=(10, 6))
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x:,.0f}"))
top_funds.plot(kind="bar", color="mediumseagreen")

# labels and title
plt.xlabel("Fund Name")
plt.ylabel("Mean Gift Amount ")
plt.title("Top 10 Funds with the Highest Average Gift Amount")
plt.xticks(rotation=45, ha="right", fontsize=10) 
plt.subplots_adjust(bottom=0.3)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()


# top 10 biggest donors
df["Constituent ID"] = df["Constituent ID"].astype(str)
top_donors = df.groupby("Constituent ID")["Gift Amount"].sum().nlargest(10)
donor_cities = df.drop_duplicates(subset=["Constituent ID"]).set_index("Constituent ID")["Location"]
city_labels = top_donors.index.map(lambda x: f"{x}\n({donor_cities.get(x, 'Unknown')})")
plt.figure(figsize=(12, 6))
# colors for bars
unique_cities = sorted(list(set(zip_locations.values())))
palette = sns.color_palette("husl", len(unique_cities))
city_colors = dict(zip(unique_cities, palette))
bar_colors = [city_colors.get(donor_cities.get(donor, "Unknown"), "gray") for donor in top_donors.index]
bars = plt.bar(city_labels, top_donors.values, color=bar_colors)
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x:,.0f}"))

# labels and title
plt.xlabel("Constituent ID")
plt.ylabel("Total Gift Amount")
plt.title("Top 10 Donors")
plt.xticks(rotation=90, ha="center", fontsize=10) 
plt.subplots_adjust(bottom=0.3)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()


# explore donors: history of top 10 donors
df["Gift Date"] = pd.to_datetime(df["Gift Date"])
df["Gift Amount"] = pd.to_numeric(df["Gift Amount"], errors="coerce")
top_donors = df.groupby("Constituent ID")["Gift Amount"].sum().nlargest(10).index
df_top = df[df["Constituent ID"].isin(top_donors)]
df_top_grouped = df_top.groupby(["Constituent ID", "Gift Date"])["Gift Amount"].sum().reset_index()
df_top_grouped = df_top_grouped.sort_values(["Constituent ID", "Gift Date"])

# plot donations over time
plt.figure(figsize=(12, 6))
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x:,.0f}"))
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


# all donations over time
df["Gift Date"] = pd.to_datetime(df["Gift Date"], errors="coerce")
df_grouped = df.groupby("Gift Date")["Gift Amount"].sum().reset_index()
df_grouped = df_grouped.set_index("Gift Date").asfreq("D", fill_value=0).reset_index()

# plot donations per year
df_yearly = df.groupby(df["Gift Date"].dt.year)["Gift Amount"].sum().reset_index()
plt.figure(figsize=(12, 6))
plt.plot(df_yearly["Gift Date"], df_yearly["Gift Amount"], marker="o", linestyle="-", color="mediumseagreen")

# labels and title
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.xlabel("Year")
plt.ylabel("Total Donations")
plt.title("Yearly Donations")
plt.xticks(df_yearly["Gift Date"])  # Show each year
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()


# think again campaign over time
df["Gift Date"] = pd.to_datetime(df["Gift Date"], errors="coerce")
df_think_again = df[df["Fund Description"] == "Think Again Capital Campaign"]
df_ta_grouped = df_think_again.groupby("Gift Date")["Gift Amount"].sum().reset_index()
df_ta_grouped = df_ta_grouped.set_index("Gift Date").asfreq("D", fill_value=0).reset_index()

# plot donations per year
df_ta_yearly = df_think_again.groupby(df_think_again["Gift Date"].dt.year)["Gift Amount"].sum().reset_index()
plt.figure(figsize=(12, 6))
plt.plot(df_ta_yearly["Gift Date"], df_ta_yearly["Gift Amount"], marker="o", linestyle="-", color="mediumseagreen")

# labels and title
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.xlabel("Year")
plt.ylabel("Total Donations")
plt.title("Think Again Campaign - Yearly Donations")
plt.xticks(df_ta_yearly["Gift Date"])  # Show each year
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()


# annual fund over time
df["Gift Date"] = pd.to_datetime(df["Gift Date"], errors="coerce")
df_fund = df[df["Fund Description"] == "Annual Fund"]
df_grouped = df_fund.groupby("Gift Date")["Gift Amount"].sum().reset_index()
df_grouped = df_grouped.set_index("Gift Date").asfreq("D", fill_value=0).reset_index()

# plot donations per year
df_yearly = df_fund.groupby(df_fund["Gift Date"].dt.year)["Gift Amount"].sum().reset_index()
plt.figure(figsize=(12, 6))
plt.plot(df_yearly["Gift Date"], df_yearly["Gift Amount"], marker="o", linestyle="-", color="mediumseagreen")

# labels and title
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.xlabel("Year")
plt.ylabel("Total Donations")
plt.title("Annual Fund - Yearly Donations")
plt.xticks(df_yearly["Gift Date"])  # Show each year
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()


# savor the story over time
df["Gift Date"] = pd.to_datetime(df["Gift Date"], errors="coerce")
df_fund = df[df["Fund Description"] == "Savor the Story"]
df_grouped = df_fund.groupby("Gift Date")["Gift Amount"].sum().reset_index()
df_grouped = df_grouped.set_index("Gift Date").asfreq("D", fill_value=0).reset_index()

# plot donations per year
df_yearly = df_fund.groupby(df_fund["Gift Date"].dt.year)["Gift Amount"].sum().reset_index()
plt.figure(figsize=(12, 6))
plt.plot(df_yearly["Gift Date"], df_yearly["Gift Amount"], marker="o", linestyle="-", color="mediumseagreen")

# labels and title
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.xlabel("Year")
plt.ylabel("Total Donations")
plt.title("Savor the Story Campaign - Yearly Donations")
plt.xticks(df_yearly["Gift Date"])  # Show each year
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()


# gala event over time
df["Gift Date"] = pd.to_datetime(df["Gift Date"], errors="coerce")
df_fund = df[df["Fund Description"] == "Gala Event"]
df_grouped = df_fund.groupby("Gift Date")["Gift Amount"].sum().reset_index()
df_grouped = df_grouped.set_index("Gift Date").asfreq("D", fill_value=0).reset_index()

# plot donations per year
df_yearly = df_fund.groupby(df_fund["Gift Date"].dt.year)["Gift Amount"].sum().reset_index()
plt.figure(figsize=(12, 6))
plt.plot(df_yearly["Gift Date"], df_yearly["Gift Amount"], marker="o", linestyle="-", color="mediumseagreen")

# labels and title
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.xlabel("Year")
plt.ylabel("Total Donations")
plt.title("Gala Event - Yearly Donations")
plt.xticks(df_yearly["Gift Date"])  # Show each year
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()


# RI family literacy initiative over time
df["Gift Date"] = pd.to_datetime(df["Gift Date"], errors="coerce")
df_fund = df[df["Fund Description"] == "RI Family Literacy Initiative"]
df_grouped = df_fund.groupby("Gift Date")["Gift Amount"].sum().reset_index()
df_grouped = df_grouped.set_index("Gift Date").asfreq("D", fill_value=0).reset_index()

# plot donations per year
df_yearly = df_fund.groupby(df_fund["Gift Date"].dt.year)["Gift Amount"].sum().reset_index()
plt.figure(figsize=(12, 6))
plt.plot(df_yearly["Gift Date"], df_yearly["Gift Amount"], marker="o", linestyle="-", color="mediumseagreen")

# labels and title
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.xlabel("Year")
plt.ylabel("Total Donations")
plt.title("RI Family Literacy Initiative - Yearly Donations")
plt.xticks(df_yearly["Gift Date"])  # Show each year
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()


# children's annual fund over time
df["Gift Date"] = pd.to_datetime(df["Gift Date"], errors="coerce")
df_fund = df[df["Fund Description"] == "Children's Annual Fund"]
df_grouped = df_fund.groupby("Gift Date")["Gift Amount"].sum().reset_index()
df_grouped = df_grouped.set_index("Gift Date").asfreq("D", fill_value=0).reset_index()

# plot donations per year
df_ta_yearly = df_fund.groupby(df_fund["Gift Date"].dt.year)["Gift Amount"].sum().reset_index()
plt.figure(figsize=(12, 6))
plt.plot(df_yearly["Gift Date"], df_yearly["Gift Amount"], marker="o", linestyle="-", color="mediumseagreen")

# labels and title
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.xlabel("Year")
plt.ylabel("Total Donations")
plt.title("Children's Annual Fund - Yearly Donations")
plt.xticks(df_yearly["Gift Date"])  # Show each year
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()