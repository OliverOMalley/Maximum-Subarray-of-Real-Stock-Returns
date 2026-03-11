# Best time to buy stock - uses Kadane's algorithm to calculate period of most consistent growth

import numpy as np

import yfinance as yf
print ("Library is Ready")

# Ask the user for a ticker 
ticker = input("Enter a stock ticker to get the best trade you could have done in the past year: ").upper()
 

#Download data

data = yf.download(ticker, period="1y", interval="1d")
company = yf.Ticker(ticker)
data_currency = company.info['currency'] 
print("This stock trades in:", data_currency)
budget = int(input("Enter how much money you want to invest :"))

data.columns = data.columns.get_level_values(0) 

print(data.head())

#Calculate daily return
data['Return'] = data['Close'].pct_change().dropna() # dropna gets rid of blank values (exist if there isnt data for the day before)
print(data['Return'])


clean_returns = data['Return'].dropna()
returns_array = clean_returns.to_numpy()   


# print(returns_array)

# (MAXIMUM SUBARRAY)
current_trade = 0
best_trade = returns_array[0]

current_start = 0
best_start = 0
best_end = 0

for day_index, daily_return in enumerate(returns_array):
    if daily_return > current_trade + daily_return:
        current_trade = daily_return # this is where we reset and start the trade again
        current_start = day_index
    else:
        current_trade = current_trade + daily_return

    if current_trade > best_trade : 
        best_trade = current_trade
        best_end = day_index
        best_start = current_start

buy_date = clean_returns.index[best_start]   
sell_date = clean_returns.index[best_end]
actual_return = budget * (1 + best_trade)

currency_symbols = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "GBp": "p",  
    "CAD": "C$",
    "JPY": "¥"
}

symbol = currency_symbols.get(data_currency, data_currency + " ")



print("-------------------------------")
print("Final value when invested in this best period of growth: ", symbol, actual_return)
print("Percentage return:", best_trade*100, "%",)
print("Buy on Day:", buy_date)
print("sell on Day:", sell_date)

# Now to make a graph to show this

import matplotlib.pyplot as plt





buy_price = data['Close'].loc[buy_date] 
sell_price = data['Close'].loc[sell_date]


plt.plot(data.index, data['Close'], label="Stock Price", color="blue", alpha=0.5)


plt.scatter(buy_date, buy_price, color="green", s=150, marker="^", label="BUY IN")
plt.scatter(sell_date, sell_price, color="red", s=150, marker="v", label="SELL OUT")


plt.title(f"{ticker} - Maximum Subarray Trade")
plt.xlabel("Date")
plt.ylabel(f"Price ({symbol})")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)


plt.show()
        
    
