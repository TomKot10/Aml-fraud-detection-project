# AML Fraud Detection Project

## Overview
This project simulates a simple Anti-Money Laundering (AML) system used to detect suspicious financial transactions.
The main goal was to go through a full data workflow — from generating raw data, through cleaning and processing, to detecting suspicious behavior and presenting results in a dashboard.
The project focuses on combining data engineering basics with analytical thinking and translating results into something useful from a business perspective.

## What I Built
- End-to-end data pipeline (from raw data to dashboard)
- Synthetic dataset with ~30,000 transactions
- Rule-based fraud detection system
- Risk scoring for each transaction
- Power BI dashboard for analysis and visualization

## Technologies
- Python (pandas, numpy, faker)
- Power BI
- Git / GitHub


## Data Pipeline

### 1. Data Generation (`generate_data.py`)
I created synthetic datasets for:
- customers
- transactions
- countries

### 2. Data Cleaning & Processing (`etl.py`)
In this step I:
- removed duplicates
- handled missing values
- standardized data formats
- created additional features like:
  - number of transactions per customer
  - average transaction amount

### 3. Fraud Detection (`aml_rules.py`)
I implemented a simple rule-based AML system inspired by real-world logic.

Each transaction is evaluated based on:
- high transaction amount
- high-risk country
- suspicious keywords in description
- unusual behavior compared to customer average
- high number of transactions

Based on this, each transaction gets:
- risk score
- alert flag (0/1)
- risk level (low / medium / high)
- explanation of why it was flagged

### 4. Analysis (`analysis.py`)
I analyzed the results to understand patterns in the data:
- distribution of risk levels
- alert rate
- alerts by country
- most risky customers
- which rules trigger most often

## Results
- ~30,000 transactions analyzed
- ~2,400 alerts detected (~8% alert rate)  
- clear patterns in high-risk countries and behaviors  
- most common triggers:
  - high-risk country
  - unusual activity patterns
  - high transaction amounts  

## Dataset
Final dataset used for analysis:
data/final/aml_dataset.csv

## Power BI Dashboard
I built an interactive dashboard that shows:
- total alerts
- alert rate (%)
- risk level distribution
- alerts by country (Top 10)
- rule trigger counts
- top high-risk customers

## Author
Tomasz Kotliński
