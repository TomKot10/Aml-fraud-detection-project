import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
from pathlib import Path

fake = Faker()

N_CUSTOMERS = 1000
N_TRANSACTIONS = 30000

countries_data = [
    ("Poland", "low"),
    ("Germany", "low"),
    ("UK", "low"),
    ("USA", "low"),
    ("Lithuania", "medium"),
    ("Czech Republic", "medium"),
    ("Turkey", "medium"),
    ("UAE", "medium"),
    ("Russia", "high"),
    ("Ukraine", "high"),
    ("Belarus", "high"),
    ("Kazakhstan", "high"),
]

countries_df = pd.DataFrame(countries_data, columns=["country", "risk_level"])

customers = []
for i in range(N_CUSTOMERS):
    customers.append({
        "customer_id": i + 1,
        "full_name": fake.name(),
        "residence_country": random.choice(countries_df["country"].tolist()),
        "customer_since": fake.date_between(start_date="-10y", end_date="today"),
        "customer_segment": random.choice(["retail", "business"]),
        "risk_profile": random.choice(["low", "medium", "high"])
    })

customers_df = pd.DataFrame(customers)

suspicious_keywords = [
    "crypto", "exchange", "cash out", "loan return",
    "consulting", "gift", "перевод", "обнал", "крипта", "обмен"
]

transactions = []
start_date = datetime.now() - timedelta(days=180)

for i in range(N_TRANSACTIONS):
    customer = customers_df.sample(1).iloc[0]

    amount = round(np.random.exponential(scale=2000), 2)
    if random.random() < 0.05:
        amount *= random.randint(5, 20)

    description = fake.sentence(nb_words=5)
    if random.random() < 0.1:
        description += " " + random.choice(suspicious_keywords)

    transactions.append({
        "transaction_id": i + 1,
        "customer_id": int(customer["customer_id"]),
        "transaction_date": start_date + timedelta(minutes=random.randint(0, 60 * 24 * 180)),
        "amount": round(amount, 2),
        "currency": "USD",
        "country": random.choice(countries_df["country"].tolist()),
        "transaction_type": random.choice(["transfer", "payment", "withdrawal"]),
        "merchant": fake.company(),
        "counterparty_name": fake.name(),
        "description": description,
        "channel": random.choice(["online", "branch", "mobile"])
    })

transactions_df = pd.DataFrame(transactions)

project_root = Path(__file__).resolve().parent.parent
output_dir = project_root / "data" / "raw"
output_dir.mkdir(parents=True, exist_ok=True)

customers_df.to_csv(output_dir / "customers.csv", index=False)
transactions_df.to_csv(output_dir / "transactions.csv", index=False)
countries_df.to_csv(output_dir / "countries.csv", index=False)

print("Dane wygenerowane poprawnie.")
print(f"Liczba klientów: {len(customers_df)}")
print(f"Liczba transakcji: {len(transactions_df)}")
print(f"Pliki zapisane w: {output_dir.resolve()}")