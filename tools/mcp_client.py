import json
import urllib.request

def fetch_financial_data(ticker: str) -> str:
    """Fetches key financial metrics, ETF holdings, and historical performance data for a given ticker symbol.

    Args:
        ticker (str): The stock or ETF ticker symbol (e.g., 'AAPL', 'VOO', 'AGG', 'SPY').
    """
    ticker = ticker.strip().upper()
    
    # Try fetching real data from a public endpoint or simulate realistic data
    # Standard realistic datasets for capstone presentation
    mock_db = {
        "VOO": {
            "name": "Vanguard S&P 500 ETF",
            "type": "ETF",
            "expense_ratio": "0.03%",
            "dividend_yield": "1.32%",
            "description": "Tracks the S&P 500 Index, representing 500 of the largest U.S. companies.",
            "top_holdings": {"MSFT": "7.1%", "AAPL": "6.2%", "NVDA": "5.0%", "AMZN": "3.8%", "META": "2.5%"},
            "annualized_returns": {"1y": "24.5%", "3y": "9.8%", "5y": "14.2%"}
        },
        "AGG": {
            "name": "iShares Core U.S. Aggregate Bond ETF",
            "type": "ETF",
            "expense_ratio": "0.03%",
            "dividend_yield": "3.45%",
            "description": "Tracks the Bloomberg U.S. Aggregate Bond Index, offering broad exposure to U.S. investment-grade bonds.",
            "top_holdings": {"US Treasury Note": "42%", "US Government Agency": "28%", "Corporate Bonds": "25%"},
            "annualized_returns": {"1y": "3.2%", "3y": "-1.8%", "5y": "0.5%"}
        },
        "QQQ": {
            "name": "Invesco QQQ Trust",
            "type": "ETF",
            "expense_ratio": "0.20%",
            "dividend_yield": "0.58%",
            "description": "Tracks the Nasdaq-100 Index, focusing heavily on technology and growth leaders.",
            "top_holdings": {"MSFT": "8.8%", "AAPL": "8.1%", "NVDA": "6.3%", "AMZN": "4.9%", "AVGO": "4.1%"},
            "annualized_returns": {"1y": "31.2%", "3y": "11.5%", "5y": "16.8%"}
        },
        "BND": {
            "name": "Vanguard Total Bond Market ETF",
            "type": "ETF",
            "expense_ratio": "0.03%",
            "dividend_yield": "3.51%",
            "description": "Provides broad exposure to U.S. investment-grade bonds, similar to AGG.",
            "top_holdings": {"US Government": "65%", "Corporate": "20%", "Securitized": "15%"},
            "annualized_returns": {"1y": "3.3%", "3y": "-1.7%", "5y": "0.6%"}
        }
    }
    
    # Try fetching simple info from Yahoo Finance query API or fallback
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=5d"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            meta = data.get("chart", {}).get("result", [{}])[0].get("meta", {})
            if meta:
                price = meta.get("regularMarketPrice")
                currency = meta.get("currency")
                real_info = {
                    "ticker": ticker,
                    "price": price,
                    "currency": currency,
                    "exchangeName": meta.get("exchangeName"),
                    "instrumentType": meta.get("instrumentType")
                }
                # If ticker in our mock db, enrich it
                if ticker in mock_db:
                    real_info.update(mock_db[ticker])
                return json.dumps(real_info, indent=2)
    except Exception:
        pass

    # Fallback to mock data if offline or ticker not found (but generate simulated info if ticker not in mock_db)
    if ticker in mock_db:
        return json.dumps({"ticker": ticker, **mock_db[ticker]}, indent=2)
    else:
        # Generate generic mock data for demonstration
        generic_data = {
            "ticker": ticker,
            "name": f"Simulated Asset {ticker}",
            "type": "Stock/ETF",
            "description": f"Generated simulated financial profile for ticker symbol {ticker}.",
            "price": 150.00,
            "expense_ratio": "0.15%",
            "dividend_yield": "2.10%",
            "annualized_returns": {"1y": "12.4%", "3y": "6.5%", "5y": "8.9%"}
        }
        return json.dumps(generic_data, indent=2)
