import os
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta

# Load the tick data
data_file_path = '~/Desktop/Daily_Ticks.csv'
# data_file_path = '~/Desktop/Daily_Ticks_20241115.csv'
data = pd.read_csv(data_file_path)
day_test = date.today()
# day_test = date(2024, 11, 21)
trading_day = (day_test - date(2024, 11, 14)).days
first_day = date(2024, 11, 20)
flag = 0


def days_ago(n):
  return (date.today() - timedelta(n)).strftime('%Y%m%d')
#   return (date(2024, 11, 18) - timedelta(n)).strftime('%Y%m%d')

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
previous_base_path = os.path.join(desktop_path, "competition_api", "Previous")
# previous_base_path = os.path.join(desktop_path, "competition_api", f"day_{trading_day - 1:02d}")

previous_portfolio_path = os.path.join(previous_base_path, "portfolio")
previous_summary_path = os.path.join(previous_base_path, "summary")
previous_statement_path = os.path.join(previous_base_path, "statement")

# Define file names with required naming convention
previous_portfolio_filename = f"024_LuckNa_portfolio.csv"
previous_statement_filename = f"024_LuckNa_statement.csv"
previous_summary_filename = f"024_LuckNa_summary.csv"
# previous_summary_filename = f"005_Na_Nhaw_summary_day{trading_day - 1}_{days_ago(4)}.csv"

previous_portfolio_path = os.path.join(previous_portfolio_path, previous_portfolio_filename)
previous_statement_path = os.path.join(previous_statement_path, previous_statement_filename)
previous_summary_path = os.path.join(previous_summary_path, previous_summary_filename)

if day_test != first_day:
    # p_portfolio = pd.read_csv(previous_portfolio_path)
    try:
        p_portfolio = pd.read_csv(previous_portfolio_path)
        if p_portfolio.empty:
            # Handle the empty file case here, e.g., create an empty DataFrame
            p_portfolio = pd.DataFrame()
            flag = 1
    except pd.errors.EmptyDataError:
        # Handle the error, e.g., create an empty DataFrame
        p_portfolio = pd.DataFrame()
        flag = 1
# p_statement = pd.read_csv(previous_statement_path)
    # p_portfolio = pd.read_csv(previous_portfolio_path)
    p_summary = pd.read_csv(previous_summary_path)
# print(p_portfolio)
# print(p_statement)
start_portfolio = {}
stock_list = data['ShareCode'].unique()

for item in stock_list:
        start_portfolio[item] = 0
# print(start_portfolio)
if day_test != first_day and flag == 0:
    
# Filter dataframe to only include rows for the stocks in stock_list
    filtered_df = p_portfolio[p_portfolio['Stock name'].isin(stock_list)]

# Create a dictionary with stock names as keys and their 'Start Vol' as values
    start_portfolio = dict(zip(filtered_df['Stock name'], filtered_df['Actual Vol']))

# Verify if all stocks in stock_list are in the dictionary; add missing stocks with volume 0
    for stock in stock_list:
        if stock not in start_portfolio:
            start_portfolio[stock] = 0  # Assign 0 or any other value for missing stocks

# # Initial funds and settingss
if day_test == first_day or day_test == date(2024, 11, 19):
    initial_cash = 10000000
else:
    initial_cash = p_summary['End Line available'][0]

data['Time'] = data['TradeDateTime']
data['Stock'] = data['ShareCode']
data['Price'] = data['LastPrice']

# Calculate the portfolio's end-of-day value
def calculate_portfolio_value():
    filtered_portfolio = [(stock, quantity) for stock, quantity in day_portfolio.items() if quantity > 0]
    return sum(quantity * data.loc[data['Stock'] == stock, 'Price'].iloc[-1] 
               for stock, quantity in filtered_portfolio)

cash_balance = initial_cash
day_portfolio = {}  # Portfolio dictionary to track stock holdings
for item in start_portfolio:
    day_portfolio[item] = start_portfolio[item]  # Portfolio dictionary to track stock holdings
buy_threshold = 50  # Example buy threshold
sell_threshold = 55  # Example sell threshold
lot_size = 100  # Buy/sell in lots of 100 shares
Match = 0
win_counter = 0
sell_buy = 0
nav = []

# Moving average settings
short_window = 180  # Short-term moving average window
long_window = 720  # Long-term moving average window
profit_target = 0.05  # 5% profit target
stop_loss = 0.03  # 3% stop loss

# Define date and file paths (same as initial export code)
today = days_ago(3)
# Define base directory path on the Desktop
# desktop_path = os.path.join("Result")
base_path = os.path.join(desktop_path, "competition_api", f"Result")
os.makedirs(base_path, exist_ok=True)


# Define paths for each file
portfolio_path = os.path.join(base_path, "portfolio")
summary_path = os.path.join(base_path, "summary")
statement_path = os.path.join(base_path, "statement")
os.makedirs(portfolio_path, exist_ok=True)
os.makedirs(summary_path, exist_ok=True)
os.makedirs(statement_path, exist_ok=True)

# Define file names with required naming convention
portfolio_filename = f"024_LuckNa_portfolio.csv"
statement_filename = f"024_LuckNa_statement.csv"
summary_filename = f"024_LuckNa_summary.csv"
# summary_filename = f"005_Na_Nhaw_summary_day{trading_day}_{today}.csv"

# Data placeholders for transactions and daily summary
transactions = []
daily_summary = []

def calculate_return_rate(nav_value):
    return ((nav_value - 10000000) / 10000000) * 100

def calculate_mean_buy_prices(transactions, stock):
    buy_prices = 0
    count = 0
    for transaction in transactions:
        if transaction['Side'] == 'B' and transaction['Stock Name'] == stock:
            buy_prices = buy_prices + transaction['Price']
            count = count + 1
    if count > 0:
        mean_buy_prices = buy_prices/count
        return mean_buy_prices
    else:
        return 0

# Helper function to calculate moving averages
def calculate_moving_averages(stock_data):
    stock_data['SMA'] = stock_data['Price'].rolling(window=short_window).mean()
    stock_data['LMA'] = stock_data['Price'].rolling(window=long_window).mean()
    
# Function to execute trades
t = 0
def execute_trade(row, stock, action, quantity, price):
    global cash_balance
    global win_counter
    global t
    global Match
    global sell_buy
    cost = quantity * price
    if action == 'buy':
        if cash_balance >= cost:
            cash_balance -= cost
            day_portfolio[stock] = day_portfolio.get(stock, 0) + quantity
            transactions.append({
                'Table Name': 'Statement_file',
                'File Name': '005_Na_Nhaw.py',
                'Stock Name': stock,
                'Date': row['Time'].split(' ')[0],
                'Time': row['Time'].split(' ')[1],  # Assuming 'Time' column exists in tick data
                'Side': 'B',
                'Volume': quantity,
                'Price': price,
                'Amount Cost': cost,
                'End Line Available': cash_balance
            })
            portfolio_value = calculate_portfolio_value()
            nav.append(portfolio_value + cash_balance)
            t = t + 1
            sell_buy = sell_buy - cost
            # print(stock, "B", t)
    elif action == 'sell':
        if day_portfolio.get(stock, 0) >= quantity:
            cash_balance += cost
            day_portfolio[stock] -= quantity
            # if day_portfolio[stock] == 0:
                # del day_portfolio[stock]  # Remove stock if holding is zero
            transactions.append({
                'Table Name': 'Statement_file',
                'File Name': '005_Na_Nhaw.py',
                'Stock Name': stock,
                'Date': row['Time'].split(' ')[0],
                'Time': row['Time'].split(' ')[1],
                'Side': 'S',
                'Volume': quantity,
                'Price': price,
                'Amount Cost': cost,
                'End Line Available': cash_balance
            })
            t = t + 1
            sell_buy = sell_buy + cost 
            Match = Match + 1
            # print(stock, "S", t)
            portfolio_value = calculate_portfolio_value()
            nav.append(portfolio_value + cash_balance)
            if price > data.loc[data['Stock'] == stock, 'Price'].mean():
                win_counter = win_counter + 1

# Process each stock individually with strategy
for stock in data['Stock'].unique():
    # print(stock)
    stock_data = data[data['Stock'] == stock].copy()
    calculate_moving_averages(stock_data)

    for index, row in stock_data.iterrows():
        price = row['Price']
        # quantity = lot_size  # Lot size for each trade
        quantity = row['Volume']  # Lot size for each trade

        if quantity > 99:
            # if quantity > 5000:
            #     quantity = 5000
            # Buy conditions: price below short moving average & not exceeding cash limit
            # if (pd.notna(row['SMA']) and price < row['SMA']) and row['Flag'] == 'Sell':
            if (pd.notna(row['SMA']) and price < row['SMA'] * 0.99) and row['Flag'] == 'Sell':
                # if quantity > 5000:
                    # quantity = 5000
                execute_trade(row, stock, 'buy', quantity, price)
                # Match = Match + 1

            # Sell conditions: 
            # - Price is above long moving average
            # - Profit target or stop loss met
            if stock in day_portfolio:
                buy_price = transactions[-1]['Price'] if transactions else price
                profit = (price - buy_price) / buy_price
                if (pd.notna(row['LMA']) and price > row['LMA'] or profit >= profit_target or profit <= -stop_loss) and row['Flag'] == 'Buy':
                # if (pd.notna(row['LMA']) and price > row['LMA'] or stop_loss <= profit <= profit_target) and row['Flag'] == 'Buy':
                    execute_trade(row, stock, 'sell', quantity, price)
                    # Match = Match + 1
    # print('test')
        
# exit(0)
# print(nav)
# print(win_counter)


realized_pl_by_stock = {}
for stock in data['Stock'].unique():
    realized_pl_by_stock[stock] = 0
buy_transactions = {}  # Dictionary to keep track of buy transactions for each stock

# Process each transaction
for transaction in transactions:
    stock = transaction['Stock Name']
    side = transaction['Side']
    price = transaction['Price']
    volume = transaction['Volume']
    
    # If the transaction is a buy, record it in buy_transactions
    if side == 'B':
        if stock not in buy_transactions:
            buy_transactions[stock] = []
        # Append a new buy transaction with price and volume
        buy_transactions[stock].append({'Price': price, 'Volume': volume})
    
    # If the transaction is a sell, calculate the realized P/L
    elif side == 'S':
        if stock in buy_transactions:
            sell_volume = volume
            sell_price = price
            
            # Process the sell transaction by matching it against stored buys
            while sell_volume > 0 and buy_transactions[stock]:
                buy_transaction = buy_transactions[stock][0]
                buy_price = buy_transaction['Price']
                buy_volume = buy_transaction['Volume']
                
                # Determine the volume to calculate P/L (match the sell with the available buy volume)
                matched_volume = min(sell_volume, buy_volume)
                
                # Calculate realized P/L for this matched volume
                pl = (sell_price - buy_price) * matched_volume
                
                # Update the cumulative realized P/L for this stock
                realized_pl_by_stock[stock] += pl
                
                # Update remaining volumes in the buy and sell transactions
                sell_volume -= matched_volume
                buy_transaction['Volume'] -= matched_volume
                
                # Remove the buy transaction if it's fully matched
                if buy_transaction['Volume'] == 0:
                    buy_transactions[stock].pop(0)
                    
# print(realized_pl_by_stock)
# print(len(realized_pl_by_stock))
# print(day_portfolio)

# print(start_portfolio)

for stock in stock_list:
    if day_portfolio[stock] == 0:
        del day_portfolio[stock]  # Remove stock if holding is zero
# print(day_portfolio)

# End-of-day portfolio summary
end_of_day_portfolio_value = calculate_portfolio_value()
daily_summary.append({
    'Table Name': 'Summary_file',
    'File Name': '005_Na_Nhaw.py',
    'trading_day' : trading_day,
    'nav' : end_of_day_portfolio_value + cash_balance,
    'end_line_available': cash_balance,
    'start_line_available': initial_cash,
    'count_Wins': win_counter,
    'count_Matched Trades': Match,
    'count_Transactions': len(transactions),
    'net_amount_today' : sell_buy,
    'Unrealized P/L': end_of_day_portfolio_value - initial_cash,
    '%Unrealized P/L': ((end_of_day_portfolio_value - initial_cash) / initial_cash) * 100,
    'Realized P/L': sum(realized_pl_by_stock.values()),
    'Maximum value': 0,
    'Minimum value': 0,
    'Win rate': 0,
    'Calmar Ratio': 0,
    'Relative Drawdown': 0,
    'Maximum Drawdown': 0,
    '%Return': 0,
})
if len(nav) == 0:
    max_value = 0
    min_value = 0
else:
    max_value = max(nav)
    min_value = min(nav)

def calculate_max_drawdown(nav_list):
    if (len(nav_list) == 0):
        return 0
    max_nav = nav_list[0]  # Start with the first NAV as the initial high
    max_drawdown = 0  # Initialize maximum drawdown

    for nav in nav_list:
        max_nav = max(max_nav, nav)  # Update the high value (max_nav)
        drawdown = (max_nav - nav) / max_nav  # Calculate drawdown from max_nav
        max_drawdown = max(max_drawdown, drawdown)  # Track the maximum drawdown
    
    return max_drawdown

if Match == 0:
    win_rate = 0
else:
    win_rate = win_counter / Match * 100

today_max_drawdown = ((end_of_day_portfolio_value + cash_balance) - 10000000) / 10000000
if day_test == first_day or day_test == date(2024, 11, 19):
    max_drawdown = today_max_drawdown
else:
    max_drawdown = min(today_max_drawdown, p_summary['Maximum Drawdown'][0])
    
max_drawdown = ((end_of_day_portfolio_value + cash_balance) - 10000000) / 10000000

if max_drawdown == 0:
    calmar_ratio = 0
else:
    calmar_ratio = calculate_return_rate(end_of_day_portfolio_value + cash_balance) / max_drawdown

if max_value == 0:
    relative_drawdown = 0
else:
    relative_drawdown = (max_drawdown / max_value) * 100

percent_return = calculate_return_rate(end_of_day_portfolio_value + cash_balance)


daily_summary[0]['Maximum value'] = max_value
daily_summary[0]['Minimum value'] = min_value
daily_summary[0]['Win rate'] = win_rate
daily_summary[0]['Calmar Ratio'] = calmar_ratio
daily_summary[0]['Relative Drawdown'] = relative_drawdown
daily_summary[0]['Maximum Drawdown'] = max_drawdown
daily_summary[0]['%Return'] = percent_return

# Save transaction log to the statement file
statement_df = pd.DataFrame(transactions)
statement_path_full = os.path.join(statement_path, statement_filename)
statement_df.to_csv(statement_path_full, index=False, float_format="%.4f")



# Save daily summary to the summary file
summary_df = pd.DataFrame(daily_summary)
summary_path_full = os.path.join(summary_path, summary_filename)
summary_df.to_csv(summary_path_full, index=False, float_format="%.4f")


# Update portfolio file with end-of-day holdings
portfolio_data = [{
    'Table Name': 'Portfolio_file',
    'File Name': '005_Na_Nhaw.py',
    'Stock Name': stock,
    'Start Vol' : start_portfolio[stock],
    'Actual Vol': quantity,
    'Avg Cost': data.loc[data['Stock'] == stock, 'Price'].mean(),
    'Market Price': data.loc[data['Stock'] == stock, 'Price'].iloc[-1],
    'Amount Cost': quantity * data.loc[data['Stock'] == stock, 'Price'].mean(),
    'Market Value': quantity * data.loc[data['Stock'] == stock, 'Price'].iloc[-1],
    'Unrealized P/L': (data.loc[data['Stock'] == stock, 'Price'].iloc[-1] - data.loc[data['Stock'] == stock, 'Price'].mean()) * quantity,
    '%Unrealized P/L': (data.loc[data['Stock'] == stock, 'Price'].iloc[-1] - data.loc[data['Stock'] == stock, 'Price'].mean())/data.loc[data['Stock'] == stock, 'Price'].mean() * 100,
    'Realized P/L': realized_pl_by_stock[stock],
} for stock, quantity in day_portfolio.items()]

portfolio_df = pd.DataFrame(portfolio_data)
portfolio_path_full = os.path.join(portfolio_path, portfolio_filename)
portfolio_df.to_csv(portfolio_path_full, index=False, float_format="%.4f")

# Format and print portfolio data   
for entry in portfolio_data:
    for item in entry:
        value = entry[item]
        if isinstance(value, float):
            print(f"{value:.4f} ", end="")  # Format as float with 4 decimal places
        else:
            print(f"{value} ", end="")  # Print as-is if not a float
    print()

# Format and print transaction data (statement)
for transaction in transactions:
    for item in transaction:
        value = transaction[item]
        if isinstance(value, float):
            print(f"{value:.4f} ", end="")  # Format as float with 4 decimal places
        else:
            print(f"{value} ", end="")  # Print as-is if not a float
    print()

# Format and print daily summary data
summary_entry = daily_summary[0]
for item in summary_entry:
    value = summary_entry[item]
    if isinstance(value, float):
        print(f"{value:.4f} ", end="")  # Format as float with 4 decimal places
    else:
        print(f"{value} ", end="")  # Print as-is if not a float