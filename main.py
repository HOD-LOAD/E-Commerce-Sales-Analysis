import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# ================================
# Step 1: Load Dataset
# ================================
csv_file = "Superstore.csv"

if not os.path.exists(csv_file):
    raise FileNotFoundError(f"❌ CSV file not found at {csv_file}. Please check the dataset path.")

df = pd.read_csv(csv_file, encoding="latin1")

print("✅ Dataset loaded successfully!\n")

# ================================
# Step 2: Data Cleaning
# ================================
df["Order Date"] = pd.to_datetime(df["Order Date"])  # ensure datetime
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

print("Shape of dataset:", df.shape)
print("\nMissing values:\n", df.isnull().sum())

# ================================
# Step 3: Load into SQLite (ETL Simulation)
# ================================
db_file = "superstore.db"
conn = sqlite3.connect(db_file)

# Replace old table if exists
df.to_sql("superstore", conn, if_exists="replace", index=False)

print(f"\n✅ Data loaded into SQLite database: {db_file}")

# ================================
# Step 4: SQL Queries
# ================================
print("\n📊 Running SQL Queries...\n")

# 1. Total Sales & Profit
query1 = """
SELECT ROUND(SUM(Sales),2) AS Total_Sales,
       ROUND(SUM(Profit),2) AS Total_Profit,
       ROUND(AVG(Discount),2) AS Avg_Discount
FROM superstore;
"""
print("💰 Overall Summary:\n", pd.read_sql(query1, conn))

# 2. Sales by Region
query2 = """
SELECT Region, ROUND(SUM(Sales),2) AS Total_Sales
FROM superstore
GROUP BY Region
ORDER BY Total_Sales DESC;
"""
print("\n🌍 Sales by Region:\n", pd.read_sql(query2, conn))

# 3. Profit by Category
query3 = """
SELECT Category, ROUND(SUM(Profit),2) AS Total_Profit
FROM superstore
GROUP BY Category
ORDER BY Total_Profit DESC;
"""
print("\n📦 Profit by Category:\n", pd.read_sql(query3, conn))

# 4. Top 5 Sub-Categories by Sales
query4 = """
SELECT "Sub-Category", ROUND(SUM(Sales),2) AS Total_Sales
FROM superstore
GROUP BY "Sub-Category"
ORDER BY Total_Sales DESC
LIMIT 5;
"""
print("\n🏆 Top 5 Sub-Categories by Sales:\n", pd.read_sql(query4, conn))

# ================================
# Step 5: Visualizations
# ================================
sns.set(style="whitegrid")

# Sales by Category
plt.figure(figsize=(8,5))
sns.barplot(x="Category", y="Sales", data=df, estimator=sum, ci=None, palette="viridis")
plt.title("Total Sales by Category")
plt.savefig("sales_by_category.png")
plt.show()

# Profit by Sub-Category
plt.figure(figsize=(12,6))
sns.barplot(x="Sub-Category", y="Profit", data=df, estimator=sum, ci=None, palette="coolwarm")
plt.xticks(rotation=45)
plt.title("Profit by Sub-Category")
plt.savefig("profit_by_subcategory.png")
plt.show()

# Region-wise Sales
plt.figure(figsize=(8,5))
sns.barplot(x="Region", y="Sales", data=df, estimator=sum, ci=None, palette="Set2")
plt.title("Sales by Region")
plt.savefig("sales_by_region.png")
plt.show()

# Sales vs Profit Scatter
plt.figure(figsize=(8,6))
sns.scatterplot(x="Sales", y="Profit", hue="Category", data=df)
plt.title("Sales vs Profit (Colored by Category)")
plt.savefig("sales_vs_profit.png")
plt.show()

# ================================
# Step 6: Time-Series Trend
# ================================
monthly_sales = df.groupby(df["Order Date"].dt.to_period("M"))["Sales"].sum()

plt.figure(figsize=(12,6))
monthly_sales.plot()
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.grid(True)
plt.savefig("monthly_sales_trend.png")
plt.show()

print("\n✅ Analysis completed. Charts saved as PNG files in project folder.")
print("✅ SQL Queries executed. Database saved as superstore.db")
