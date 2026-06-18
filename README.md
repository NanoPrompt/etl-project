# Universal Crypto Market ETL Pipeline

A lightweight, automated End-to-End (ETL) data pipeline that extracts real-time cryptocurrency market data, transforms it with volatility risk metrics, and concurrently distributes the cleaned payload locally for GitHub tracking and upstream via REST API to GitLab.

## 🚀 Architecture Overview

This project implements a **Universal Distribution Architecture**. Instead of relying on traditional Git remotes for dual-pushing, the core pipeline script itself interacts directly with cloud version control environments via secure APIs.

* **Extract:** Pulls live market metrics (ticker, closing price, volume, market cap, price change percentage) for the top 50 cryptocurrencies using the TradingView Screener API.
* **Transform:** Cleans schemas, normalizes data formats, and evaluates a custom `Risk_Profile` column flagging assets with high price fluctuations.
* **Load (Dual Destination):**
  * **Local Destination:** Writes a structured JSON payload to the local directory for traditional Git versioning (GitHub).
  * **Cloud Destination:** Calls the GitLab Commits API directly to instantly sync and version the live data within the cloud repository.

---

## 🛠️ Project Structure

```text
etl-project/
│
├── .gitlab-ci.yml                 # GitLab CI/CD pipeline automation config
├── cleaned_crypto_market_data.json # The generated/transformed target payload
├── market_etl_pipeline.py         # Main Python ETL script execution logic
└── requirements.txt               # Project dependencies