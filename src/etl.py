import pandas as pd
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent

customers_file = base_path / "data" / "raw" / "customers.csv"
transactions_file = base_path / "data" / "raw" / "transactions.csv"
countries_file = base_path / "data" / "raw" / "countries.csv"

def load_csv(path):
    try:
        df = pd.read_csv(path, sep=";", encoding="utf-8-sig")
    except UnicodeDecodeError:
        df = pd.read_csv(path, sep=";", encoding="latin1")
    return df

print("Start ETL")

customers = load_csv(customers_file)
transactions = load_csv(transactions_file)
countries = load_csv(countries_file)

customers.columns = customers.columns.str.strip()
transactions.columns = transactions.columns.str.strip()
countries.columns = countries.columns.str.strip()

print("Files loaded")
print("Customers shape:", customers.shape)
print("Transactions shape:", transactions.shape)
print("Countries shape:", countries.shape)

print("\nTransactions columns:")
print(transactions.columns.tolist())

# type fixes
transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"],
    errors="coerce"
)

transactions["amount"] = pd.to_numeric(
    transactions["amount"],
    errors="coerce"
)

transactions["customer_id"] = pd.to_numeric(
    transactions["customer_id"],
    errors="coerce"
)

customers["customer_id"] = pd.to_numeric(
    customers["customer_id"],
    errors="coerce"
)

customers = customers.drop_duplicates()
transactions = transactions.drop_duplicates()
countries = countries.drop_duplicates()

print("\nMissing values in transactions:")
print(transactions.isna().sum())

# remove rows with missing key values
transactions = transactions.dropna(subset=["transaction_date", "amount", "customer_id"])
customers = customers.dropna(subset=["customer_id"])

# convert ids to int after cleaning
transactions["customer_id"] = transactions["customer_id"].astype(int)
customers["customer_id"] = customers["customer_id"].astype(int)

transactions = transactions[transactions["amount"] >= 0]
transactions = transactions[transactions["customer_id"].isin(customers["customer_id"])]

trans_per_customer = transactions.groupby("customer_id").size()
avg_amount_per_customer = transactions.groupby("customer_id")["amount"].mean()

transactions["transactions_count"] = transactions["customer_id"].map(trans_per_customer)
transactions["avg_amount_customer"] = transactions["customer_id"].map(avg_amount_per_customer)
transactions["high_amount_flag"] = (transactions["amount"] > 10000).astype(int)

output_folder = base_path / "data" / "processed"
output_folder.mkdir(parents=True, exist_ok=True)

customers.to_csv(output_folder / "customers_clean.csv", index=False)
transactions.to_csv(output_folder / "transactions_clean.csv", index=False)
countries.to_csv(output_folder / "countries_clean.csv", index=False)

print("\nETL done")
print("Saved in:", output_folder)
print("Final transactions shape:", transactions.shape)