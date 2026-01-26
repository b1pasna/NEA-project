import requests
import pandas as pd
import time # adding delays between requests

def fetch_crypto_tickers():
    #fetches the first 10 pages of cryptocurrency tickers from CoinGecko API 
    url = "https://api.coingecko.com/api/v3/coins/markets" # api endpoiint to fetch market data
    all_data = []
    max_pages = 10  
    max_per_page = 250
    max_attempts = 3

# loop through pages 1 to 10
    for page in range(1, max_pages + 1):
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": max_per_page,
            "page": page
        }

        for attempt in range(max_attempts):
            try:
                response = requests.get(url, params=params)
                response.raise_for_status() # error raised for bad response

                data = response.json()
                if not data:
                    break

                all_data.extend([{"ticker": f"{coin['symbol'].upper()}-USD", "name": coin['name']} for coin in data])
                print(f"Page {page} fetched successfully.")

                # avoid api rate limits
                time.sleep(1.5) 
                break

            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    print("Rate limit reached. Sleeping for 60 seconds...")
                    time.sleep(60)
                else:
                    print(f"Error fetching data on page {page}: {e}")
                    return pd.DataFrame(all_data)

    # convert the list to panda df
    df = pd.DataFrame(all_data)
    # save datafrane to csv
    output_file = "cryptoTickers.csv"
    df.to_csv(output_file, index=False)
    print(f"Data successfully written to '{output_file}'. Total tickers: {len(df)}")
    return df

# fetch and display the first few rows
tickers_df = fetch_crypto_tickers()
display(tickers_df.head())
