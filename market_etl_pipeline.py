import os
import json
import base64
import pandas as pd
import requests
from tradingview_screener import crypto, Query

# ==========================================
# CONFIGURATION (Replace with your own data)
# ==========================================
GITLAB_TOKEN = "your_gitlab_personal_access_token"
GITLAB_PROJECT_ID = "your_project_id" # E.g., '12345678'
GITLAB_BRANCH = "main"
TARGET_FILE_NAME = "cleaned_crypto_market_data.json"

def run_trading_etl():
    print("🚀 Initializing TradingView to GitLab ETL Pipeline...")
    print("-" * 50)

    # ==========================================
    # STEP 1: EXTRACT
    # ==========================================
    print("[1/3] EXTRACT: Fetching Crypto data from TradingView Screener...")
    try:
        # Querying live screener data directly bypassing web blocks
        raw_df = (crypto()
                  .select('name', 'close', 'volume', 'market_cap_basic', 'change')
                  .limit(50)
                  .get_scanner_data()[1]) # Get the DataFrame element from the tuple
        
        print(f"✔ Success! Extracted {len(raw_df)} rows from TradingView.")
    except Exception as e:
        print(f"❌ Extraction Failed: {e}")
        return

    # ==========================================
    # STEP 2: TRANSFORM
    # ==========================================
    print("\n[2/3] TRANSFORM: Cleaning and enriching financial data...")
    try:
        # Drop rows with critical missing numbers (e.g., Market Cap)
        df_clean = raw_df.dropna(subset=['market_cap_basic', 'close']).copy()
        
        # Rename columns to look professional
        df_clean.rename(columns={
            'name': 'Ticker',
            'close': 'Closing_Price',
            'volume': 'Volume',
            'market_cap_basic': 'Market_Cap',
            'change': 'Price_Change_Percent'
        }, inplace=True)
        
        # Enrichment: Calculate an Arbitrary Risk Indicator based on Volatility/Change 
        # (High Risk if daily swing is over 4% or under -4%)
        df_clean['Risk_Profile'] = df_clean['Price_Change_Percent'].apply(
            lambda x: 'High Volatility' if abs(x) > 4 else 'Stable'
        )
        
        # Formatting data into an oriented JSON string format for web consumption
        transformed_json = df_clean.to_json(orient='records', indent=4)
        print(f"✔ Success! Transformation complete. Ready to load {len(df_clean)} items.")
    except Exception as e:
        print(f"❌ Transformation Failed: {e}")
        return

    # ==========================================
    # STEP 3: LOAD (GitLab API Commit)
    # ==========================================
    print(f"\n[3/3] LOAD: Pushing target payload to GitLab repository...")
    
    # GitLab API endpoint to create/update files directly via Commits
    url = f"https://gitlab.com/api/v4/projects/{GITLAB_PROJECT_ID}/repository/commits"
    
    headers = {
        "PRIVATE-TOKEN": GITLAB_TOKEN,
        "Content-Type": "application/json"
    }
    
    # We construct a single commit payload containing an 'update' or 'create' action
    payload = {
        "branch": GITLAB_BRANCH,
        "commit_message": "Feat: Automated ETL Sync - Uploaded latest TradingView data",
        "actions": [
            {
                "action": "update", # Defaults to update; handles fallback to create automatically below
                "file_path": TARGET_FILE_NAME,
                "content": transformed_json
            }
        ]
    }
    
    # Check if file exists first to safely toggle action type if needed
    file_check_url = f"https://gitlab.com/api/v4/projects/{GITLAB_PROJECT_ID}/repository/files/{TARGET_FILE_NAME}?ref={GITLAB_BRANCH}"
    check_response = requests.get(file_check_url, headers={"PRIVATE-TOKEN": GITLAB_TOKEN})
    
    if check_response.status_code == 404:
        payload["actions"][0]["action"] = "create" # Switch to create action if file is absent

    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code in [200, 201]:
            print("-" * 50)
            print("🎉 ETL PIPELINE SUCCESSFUL!")
            print(f"File '{TARGET_FILE_NAME}' successfully loaded into GitLab branch '{GITLAB_BRANCH}'.")
        else:
            print(f"❌ Load Failed! GitLab API Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Network error pushing to GitLab: {e}")

if __name__ == "__main__":
    run_trading_etl()