import sys
import pandas as pd
import matplotlib.pyplot as plt

# Fix encoding issue in terminal
sys.stdout.reconfigure(encoding="utf-8")

# Load dataset
df = pd.read_csv("project_2/data/cleaned_ecommerce.csv", encoding="utf-8")

# Convert Rating to numeric (important fix)
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

# Drop rows with missing rating or date
df = df.dropna(subset=["Rating", "Review Date"])

# =========================
# 1. Average Rating
# =========================
average_rating = df["Rating"].mean()
print("Average Rating:", round(average_rating, 2))

# =========================
# 2. Sentiment Analysis
# =========================
def sentiment(x):
    if x >= 4:
        return "Positive"
    elif x == 3:
        return "Neutral"
    else:
        return "Negative"

df["Sentiment"] = df["Rating"].apply(sentiment)

# Sentiment count
sentiment_counts = df["Sentiment"].value_counts()
print("\nSentiment Count:")
print(sentiment_counts)

# Sentiment percentage
sentiment_percent = df["Sentiment"].value_counts(normalize=True) * 100
print("\nSentiment Percentage:")
print(sentiment_percent.round(2))

# =========================
# 3. Sentiment Bar Chart
# =========================
sentiment_counts.plot(kind="bar", figsize=(6, 4))
plt.title("Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Count")
plt.grid(axis="y")
plt.show()

# =========================
# 4. Date Processing
# =========================
df["Review Date"] = pd.to_datetime(df["Review Date"], errors="coerce")
df = df.dropna(subset=["Review Date"])

df["Month"] = df["Review Date"].dt.month

# Monthly review count
monthly_reviews = df.groupby("Month")["Rating"].count().sort_index()

print("\nMonthly Review Count:")
print(monthly_reviews)

# =========================
# 5. Monthly Trend Line Chart
# =========================
monthly_reviews.plot(kind="line", marker="o", figsize=(7, 4))
plt.title("Monthly Review Trend")
plt.xlabel("Month")
plt.ylabel("Number of Reviews")
plt.grid()
plt.show()

# =========================
# 6. Insights Section
# =========================
print("\nINSIGHTS:")
print("1. Most common rating:", df["Rating"].mode()[0])
print("2. Total reviews:", len(df))
print("3. Positive %:", round((df["Sentiment"] == "Positive").mean() * 100, 2))

# =========================
# 7. Save Cleaned File (IMPORTANT for Power BI)
# =========================
df.to_csv("cleaned_data_for_powerbi.csv", index=False)

print("\nCleaned file saved successfully!")