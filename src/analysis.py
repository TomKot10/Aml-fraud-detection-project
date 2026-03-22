import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent

file = base_path / "data" / "aml" / "transactions_flagged.csv"

df = pd.read_csv(file)

print("Data loaded:", df.shape)


#BASIC STATS


print("\nRisk level distribution:")
print(df["aml_risk_level"].value_counts())

print("\nAlert count:")
print(df["alert_flag"].value_counts())


# ALERTS PER COUNTRY


alerts_country = (
    df[df["alert_flag"] == 1]
    .groupby("country")
    .size()
    .sort_values(ascending=False)
)

print("\nAlerts per country:")
print(alerts_country.head(10))


# TOP CUSTOMERS


top_customers = (
    df.groupby("customer_id")["risk_score"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop risky customers:")
print(top_customers)


# RULE USAGE


rules = [
    "rule_high_amount",
    "rule_high_risk_country",
    "rule_suspicious_description",
    "rule_amount_vs_avg",
    "rule_many_transactions"
]

rule_counts = df[rules].sum().sort_values(ascending=False)

print("\nRule triggers:")
print(rule_counts)


# PLOTS


plots_dir = base_path / "data" / "plots"
plots_dir.mkdir(parents=True, exist_ok=True)

# 1. risk score histogram
plt.figure()
df["risk_score"].hist(bins=50)
plt.title("Risk Score Distribution")
plt.xlabel("risk_score")
plt.ylabel("count")
plt.savefig(plots_dir / "risk_score_hist.png")

# 2. alerts per country
plt.figure()
alerts_country.head(10).plot(kind="bar")
plt.title("Top countries by alerts")
plt.ylabel("alerts")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(plots_dir / "alerts_country.png")

# 3. rule usage
plt.figure()
rule_counts.plot(kind="bar")
plt.title("Rule triggers")
plt.ylabel("count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(plots_dir / "rules.png")

print("\nPlots saved in:", plots_dir)


# EXPORT POWER BI


final_dir = base_path / "data" / "final"
final_dir.mkdir(parents=True, exist_ok=True)

df.to_csv(final_dir / "aml_dataset.csv", index=False, sep=",")

print("\nFinal dataset saved for Power BI")