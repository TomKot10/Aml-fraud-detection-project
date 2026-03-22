import pandas as pd
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent

transactions_file = base_path / "data" / "processed" / "transactions_clean.csv"
countries_file = base_path / "data" / "processed" / "countries_clean.csv"

transactions = pd.read_csv(transactions_file)
countries = pd.read_csv(countries_file)

transactions.columns = transactions.columns.str.strip()
countries.columns = countries.columns.str.strip()

transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"],
    errors="coerce"
)

transactions["amount"] = pd.to_numeric(
    transactions["amount"],
    errors="coerce"
)

transactions["avg_amount_customer"] = pd.to_numeric(
    transactions["avg_amount_customer"],
    errors="coerce"
)

transactions["transactions_count"] = pd.to_numeric(
    transactions["transactions_count"],
    errors="coerce"
)

transactions = transactions.merge(countries, on="country", how="left")

keywords = [
    "crypto", "exchange", "cash out", "loan return",
    "consulting", "gift", "перевод", "обнал", "крипта", "обмен"
]

transactions["description_lower"] = transactions["description"].fillna("").str.lower()

transactions["rule_high_amount"] = (transactions["amount"] > 10000).astype(int)

transactions["rule_high_risk_country"] = (
    transactions["risk_level"] == "high"
).astype(int)

transactions["rule_suspicious_description"] = transactions["description_lower"].apply(
    lambda x: int(any(word in x for word in keywords))
)

transactions["rule_amount_vs_avg"] = (
    transactions["amount"] > transactions["avg_amount_customer"] * 3
).astype(int)

transactions["rule_many_transactions"] = (
    transactions["transactions_count"] > 40
).astype(int)

transactions["risk_score"] = (
    transactions["rule_high_amount"] * 30 +
    transactions["rule_high_risk_country"] * 25 +
    transactions["rule_suspicious_description"] * 20 +
    transactions["rule_amount_vs_avg"] * 15 +
    transactions["rule_many_transactions"] * 10
)

def get_risk_level(score):
    if score >= 60:
        return "high"
    elif score >= 30:
        return "medium"
    return "low"

transactions["aml_risk_level"] = transactions["risk_score"].apply(get_risk_level)
transactions["alert_flag"] = (transactions["risk_score"] >= 30).astype(int)

def get_reason(row):
    reasons = []

    if row["rule_high_amount"] == 1:
        reasons.append("high amount")
    if row["rule_high_risk_country"] == 1:
        reasons.append("high risk country")
    if row["rule_suspicious_description"] == 1:
        reasons.append("suspicious description")
    if row["rule_amount_vs_avg"] == 1:
        reasons.append("amount above avg")
    if row["rule_many_transactions"] == 1:
        reasons.append("many transactions")

    return ", ".join(reasons)

transactions["alert_reason"] = transactions.apply(get_reason, axis=1)

output_folder = base_path / "data" / "aml"
output_folder.mkdir(parents=True, exist_ok=True)

transactions.to_csv(output_folder / "transactions_flagged.csv", index=False)

print("AML rules done")
print("Saved in:", output_folder)
print("\nRisk level counts:")
print(transactions["aml_risk_level"].value_counts())

print("\nAlert flag counts:")
print(transactions["alert_flag"].value_counts())