import os
import json
import pandas as pd
from tradingview_screener import crypto, Query

# ==========================================
# CONFIGURATION
# ==========================================
TARGET_FILE_NAME = "cleaned_crypto_market_data.json"

def run_trading_etl():
    print("🚀 Initializing TradingView to GitHub ETL Pipeline...")
    print("-" * 50)

    # ==========================================
    # STEP 1: EXTRACT
    # ==========================================
    print("[1/3] EXTRACT: Fetching Crypto data from TradingView Screener...")
    try:
        raw_df = (crypto()
                  .select('name', 'close', 'volume', 'market_cap_basic', 'change')
                  .limit(50)
                  .get_scanner_data()[1])
        
        print(f"✔ Success! Extracted {len(raw_df)} rows from TradingView.")
    except Exception as e:
        print(f"❌ Extraction Failed: {e}")
        return

    # ==========================================
    # STEP 2: TRANSFORM
    # ==========================================
    print("\n[2/3] TRANSFORM: Cleaning and enriching financial data...")
    try:
        df_clean = raw_df.copy()
        
        df_clean.rename(columns={
            'name': 'Ticker',
            'close': 'Closing_Price',
            'volume': 'Volume',
            'market_cap_basic': 'Market_Cap',
            'change': 'Price_Change_Percent'
        }, inplace=True)
        
        df_clean['Risk_Profile'] = df_clean['Price_Change_Percent'].apply(
            lambda x: 'High Volatility' if abs(x) > 4 else 'Stable'
        )
        
        print(f"✔ Success! Transformation complete. Ready to save {len(df_clean)} items.")
    except Exception as e:
        print(f"❌ Transformation Failed: {e}")
        return

    # ==========================================
    # STEP 3: LOAD (Save Locally for Git tracking)
    # ==========================================
    print(f"\n[3/3] LOAD: Saving target payload locally to '{TARGET_FILE_NAME}'...")
    try:
        # Save directly to your local project folder
        df_clean.to_json(TARGET_FILE_NAME, orient='records', indent=4)
        print("-" * 50)
        print("🎉 LOCAL ETL PIPELINE SUCCESSFUL!")
        print(f"File '{TARGET_FILE_NAME}' is ready to be pushed to GitHub.")
    except Exception as e:
        print(f"❌ Local Load Failed: {e}")

if __name__ == "__main__":
    run_trading_etl()