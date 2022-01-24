# Stonkleton
CLI to provide users with the intrinsic value of stocks.
Data is obtained from Yahoo Finance and used in an instrinic value model.

# To Do
- Telegram Bot 
    - Features:
        Send ticker -> return estimated discount rate and expected IV
        User watchlist; /scan to iterate with send ticker function

- Add a range of expected earnings estimates
    - Get 5Y EPS growth estimate from Zachs (via Scrapy)

# Features Roadmap
- Screener
    - IVx, TA
- Add more fundamental calculations
- Notification system
- Options
    - Begin with wheeling

# Long Term Goal
1. Have a list of stocks on watchlist
2. Get stock alert based on price movement
    - rules need to be quantified
3. Determine what type of trade to make
    - long/short, credit/debit
4. Recommend trade to user
