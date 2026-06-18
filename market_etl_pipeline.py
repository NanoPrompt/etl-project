import os
import json
import pandas as pd
import requests
from tradingview_screener import crypto, Query

# ==========================================
# CONFIGURATION
# ==========================================
# GitLab specific configs
GITLAB_TOKEN = os.getenv("GITLAB_COMMON_TOKEN")
GITLAB_PROJECT_ID = os.getenv("CI_PROJECT_ID", "83521314")  # Fallback to your explicit Project ID

GITLAB_BRANCH = "main"

# Shared config
TARGET_FILE_NAME = "cleaned_crypto_market_data.json"

def run_trading_etl():
    print("🚀 Initializing Universal GitHub & GitLab ETL Pipeline...")
    print("-" * 50)

    # ==========================================
    # STEP 1: EXTRACT
    # ==========================================
    print("[1/3] EXTRACT: Fetching Crypto data from TradingView...")
    try:
        raw_df = (crypto()
                  .select('name', 'close', 'volume', 'market_cap_basic', 'change')
                  .limit(50)
                  .get_scanner_data()[1])
        print(f"✔ Success! Extracted {len(raw_df)} rows.")
    except Exception as e:
        print(f"❌ Extraction Failed: {e}")
        return

    # ==========================================
    # STEP 2: TRANSFORM
    # ==========================================
    print("\n[2/3] TRANSFORM: Cleaning and enriching data...")
    try:
        df_clean = raw_df.copy()
        df_clean.rename(columns={
            'name': 'Ticker', 'close': 'Closing_Price', 'volume': 'Volume',
            'market_cap_basic': 'Market_Cap', 'change': 'Price_Change_Percent'
        }, inplace=True)
        
        df_clean['Risk_Profile'] = df_clean['Price_Change_Percent'].apply(
            lambda x: 'High Volatility' if abs(x) > 4 else 'Stable'
        )
        transformed_json = df_clean.to_json(orient='records', indent=4)
        print(f"✔ Success! Transformation complete. Ready to load {len(df_clean)} items.")
    except Exception as e:
        print(f"❌ Transformation Failed: {e}")
        return

    # ==========================================
    # STEP 3: LOAD (Both GitHub & GitLab)
    # ==========================================
    print(f"\n[3/3] LOAD: Distributing target payload...")

    # --- Destination A: GitHub (Save locally for local git tracking) ---
    try:
        df_clean.to_json(TARGET_FILE_NAME, orient='records', indent=4)
        print(f"✔ Destination GitHub: Saved locally to '{TARGET_FILE_NAME}'")
    except Exception as e:
        print(f"❌ GitHub Local Save Failed: {e}")

    # --- Destination B: GitLab (Upload to cloud via API) ---
    if not GITLAB_TOKEN:
        print("⚠ Destination GitLab: Skipped (Token missing from system environment variables).")
        return

    url = f"https://gitlab.com/api/v4/projects/{GITLAB_PROJECT_ID}/repository/commits"
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN, "Content-Type": "application/json"}
    
    payload = {
        "branch": GITLAB_BRANCH,
        "commit_message": "Feat: Automated ETL Sync - Uploaded latest TradingView data",
        "actions": [{"action": "update", "file_path": TARGET_FILE_NAME, "content": transformed_json}]
    }
    
    # Toggle between creating a new file or updating an existing file on GitLab
    file_check_url = f"https://gitlab.com/api/v4/projects/{GITLAB_PROJECT_ID}/repository/files/{TARGET_FILE_NAME}?ref={GITLAB_BRANCH}"
    check_response = requests.get(file_check_url, headers={"PRIVATE-TOKEN": GITLAB_TOKEN})
    if check_response.status_code == 404:
        payload["actions"][0]["action"] = "create"

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in [200, 201]:
            print("✔ Destination GitLab: Successfully pushed to cloud repository!")
        else:
            print(f"❌ Destination GitLab: Cloud Upload Failed ({response.status_code} - {response.text})")
    except Exception as e:
        print(f"❌ Destination GitLab: Network error: {e}")

    print("-" * 50)
    print("🎉 UNIVERSAL ETL PIPELINE COMPLETED WORK!")

if __name__ == "__main__":
    run_trading_etl()