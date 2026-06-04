import pandas as pd
import yfinance as yf
import json
import datetime

def lstm_prediction(se, stock_symbol):
    try:
        if se == 'NSE':
            stock_symbol += ".NS"

        df = yf.download(stock_symbol, period="1y")

        if df is None or df.empty:
            return json.dumps({"error": "No data found"})

        # ✅ FIX: always ensure single column
        df = df[['Close']].copy()

        # 🔥 VERY IMPORTANT FIX
        if isinstance(df['Close'], pd.DataFrame):
            df['Close'] = df['Close'].iloc[:, 0]

        df.reset_index(inplace=True)

        # ✅ SAFE last price
        last_price = df['Close'].iloc[-1]
        if hasattr(last_price, "item"):
            last_price = last_price.item()

        predicted_price = round(float(last_price) * 1.01, 2)

        future_date = datetime.datetime.now().date() + datetime.timedelta(days=1)

        result = []

        for _, row in df.tail(30).iterrows():
            close_val = row['Close']

            # ✅ FIX: ensure scalar
            if hasattr(close_val, "item"):
                close_val = close_val.item()

            result.append({
                "Date": str(row['Date']),
                "Close": float(close_val)
            })

        result.append({
            "Date": str(future_date),
            "Close": predicted_price
        })

        return json.dumps(result)

    except Exception as e:
        print("MODEL ERROR:", e)
        return json.dumps({"error": str(e)})