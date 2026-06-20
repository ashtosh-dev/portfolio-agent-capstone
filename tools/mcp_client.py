import json
import yfinance as yf

def fetch_financial_data(ticker: str) -> str:
    """Fetches key live financial metrics and description for a given stock or ETF ticker symbol from Yahoo Finance.

    Args:
        ticker (str): The stock or ETF ticker symbol (e.g., 'AAPL', 'VOO', 'AGG', 'SPY').
    """
    ticker = ticker.strip().upper()
    try:
        t = yf.Ticker(ticker)
        info = t.info or {}
        
        # Determine regularMarketPrice with fallback options
        price = info.get("regularMarketPrice")
        if price is None:
            price = info.get("currentPrice")
        if price is None:
            price = info.get("navPrice")
        if price is None:
            # Last available closing price from history
            hist = t.history(period="1d")
            if not hist.empty:
                price = float(hist["Close"].iloc[-1])
        
        # Assemble dictionary with default fallbacks
        data = {
            "ticker": ticker,
            "longName": info.get("longName") or info.get("shortName") or "N/A",
            "regularMarketPrice": price if price is not None else "N/A",
            "yield": info.get("dividendYield") if info.get("dividendYield") is not None else "N/A",
            "ytdReturn": info.get("ytdReturn") if info.get("ytdReturn") is not None else "N/A",
            "fiveYearAverageReturn": info.get("fiveYearAverageReturn") if info.get("fiveYearAverageReturn") is not None else "N/A",
            "businessSummary": info.get("longBusinessSummary") or info.get("shortBusinessSummary") or "N/A"
        }
        return json.dumps(data, indent=2)
    except Exception as e:
        # Gracefully return N/A fields on error
        return json.dumps({
            "ticker": ticker,
            "error": str(e),
            "longName": "N/A",
            "regularMarketPrice": "N/A",
            "yield": "N/A",
            "ytdReturn": "N/A",
            "fiveYearAverageReturn": "N/A",
            "businessSummary": "N/A"
        }, indent=2)
