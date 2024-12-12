import pandas as pd
import numpy as np
import os
from datetime import datetime
from datetime import time
from ta.momentum import RSIIndicator

################################################################################################################################

team_name = '024_LuckNa'

################################################################################################################################

output_dir = os.path.expanduser("~/Desktop/competition_api_new")
if not os.path.exists(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    print(f"Created main directory: {output_dir}")

def load_previous(file_type, teamName):
    output_dir = os.path.expanduser("~/Desktop/competition_api_new")
    folder_path = os.path.join(output_dir, "Previous", file_type)
    file_path = os.path.join(folder_path, f"{teamName}_{file_type}.csv")
    
    if os.path.exists(file_path):
        try:
            data = pd.read_csv(file_path)
            print(f"Loaded '{file_type}' data for team {teamName}.")
            return data
        except Exception as e:
            print(f"Error loading file: {e}")
            return None
    else:
        print(f"File not found: {file_path}")
        return None

def save_output(data, file_type, teamName):
    folder_path = output_dir + f"/Result/{file_type}"
    file_path = folder_path + f"/{teamName}_{file_type}.csv"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
        print(f"Directory created: '{folder_path}'")

    # Save CSV
    data.to_csv(file_path, index=False)
    print(f"{file_type} saved at {file_path}")

def calculate_rsi(data, period=14):
    """Calculate the RSI for a given dataset."""
    delta = data['Close'].diff()  # Calculate daily price changes
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()  # Average gain
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()  # Average loss
    
    rs = gain / loss  # Relative Strength
    rsi = 100 - (100 / (1 + rs))  # RSI formula
    return rsi

statements = []

file_path = os.path.expanduser('~/Desktop/Daily_Ticks.csv') 
df = pd.read_csv(file_path)

initial_investment = 10000000 

# Load the summary file
prev_summary_df = load_previous("summary", team_name)

if prev_summary_df is not None:
    if 'End Line available' in prev_summary_df.columns:
        # ดึงค่าคอลัมน์ 'End Line available' ทั้งหมด
        initial_balance_series = prev_summary_df['End Line available']
        
        # ตรวจสอบว่าคอลัมน์ไม่ว่างเปล่า
        if not initial_balance_series.empty:
            # เข้าถึงค่าแรกของคอลัมน์
            first_value = initial_balance_series.iloc[0]
            
            # ลบเครื่องหมายคั่นหลักพันและแปลงเป็น float
            try:
                initial_balance = float(str(first_value).replace(',', '').strip())
                Start_Line_available = initial_balance
                print("End Line available column loaded successfully.")
                print(f"Initial balance (first value): {initial_balance}")
            except ValueError:
                print(f"Error converting '{first_value}' to a float.")
                initial_balance = initial_investment  # ใช้ค่าตั้งต้นในกรณีเกิดข้อผิดพลาด
        else:
            print("'End Line available' column is empty.")
            initial_balance = initial_investment  # ใช้ค่าตั้งต้นหากคอลัมน์ว่าง
    else:
        print("'End Line available' column not found in the file.")
        initial_balance = initial_investment  # ใช้ค่าตั้งต้นหากไม่มีคอลัมน์
else:
    initial_balance = initial_investment  # ใช้ค่าตั้งต้นหากไฟล์ไม่โหลด
    Start_Line_available = initial_investment
    print(f"Initial balance = initial_investment: {initial_investment}")

################################################################################################################################

# Calculate RSI using the 'LastPrice' column
rsi_period = 14
df['RSI'] = RSIIndicator(close=df['LastPrice'], window=rsi_period).rsi()
# df['RSI'] = calculate_rsi(df, rsi_period)
# print(f'RSI : {df['RSI']}')


# Add trading conditions
buy_threshold = 30
sell_threshold = 70

# Initialize trading variables
initial_investment = 10000000
balance = initial_investment
portfolio = 0  # Shares held
portfolio_value = 0
last_price = 0

# Dictionaries for portfolio and statement
portfolio_data = {
    'Table Name': [],
    'File Name': [],
    'Stock name': [],
    'Start Vol': [],
    'Actual Vol': [],
    'Avg Cost': [],
    'Market Price': [],
    'Market Value': [],
    'Amount Cost': [],
    'Unrealized P/L': [],
    '% Unrealized P/L': [],
    'Realized P/L': []
}

statement_data = {
    'Table Name': [],
    'File Name': [],
    'Stock Name': [],
    'Date': [],
    'Time': [],
    'Side': [],
    'Volume': [],
    'Price': [],
    'Amount Cost': [],
    'End Line Available': []
}

# List of variable trading volumes
volume_options = [100, 200, 300, 500]

# Trading loop
for index, row in df.iterrows():
    stock_name = row['ShareCode']
    price = row['LastPrice']
    rsi = row['RSI']
    date_time = row['TradeDateTime']
    # volume = row['Volume']

    # Split date and time
    date = date_time.split()[0]
    time = date_time.split()[1]

    # Randomly select a volume for each trade
    volume = np.random.choice(volume_options)
    # Buy condition
    if rsi < buy_threshold and balance >= price * volume:
        # print('less than')
        cost = price * volume
        balance -= cost
        portfolio += volume
        last_price = price

        # Log the trade in the statement
        statement_data['Table Name'].append('Statement_file')
        statement_data['File Name'].append(team_name)
        statement_data['Stock Name'].append(stock_name)
        statement_data['Date'].append(date)
        statement_data['Time'].append(time)
        statement_data['Side'].append('Buy')
        statement_data['Volume'].append(volume)
        statement_data['Price'].append(price)
        statement_data['Amount Cost'].append(cost)
        statement_data['End Line Available'].append(balance)

    # Sell condition
    elif rsi > sell_threshold and portfolio > 0:
        # print('more than')
        revenue = price * portfolio
        balance += revenue
        profit = (price - last_price) * portfolio
        portfolio = 0

        # Log the trade in the statement
        statement_data['Table Name'].append('Statement_file')
        statement_data['File Name'].append(team_name)
        statement_data['Stock Name'].append(stock_name)
        statement_data['Date'].append(date)
        statement_data['Time'].append(time)
        statement_data['Side'].append('Sell')
        statement_data['Volume'].append(volume)
        statement_data['Price'].append(price)
        statement_data['Amount Cost'].append(revenue)
        statement_data['End Line Available'].append(balance)

# Create DataFrames
portfolio_df = pd.DataFrame(portfolio_data)
statement_df = pd.DataFrame(statement_data)

summary_data = {
    'Table Name': ['Summary_file'],
    'File Name': [team_name],
    'NAV': [balance + portfolio * last_price],  # Net Asset Value
    'Portfolio value': [portfolio * last_price],
    'End Line available': [balance],
    'Number of wins': [0],  # Update logic to count wins
    'Number of matched trades': [len(statement_df)],  # Total trades
    'Unrealized P/L': [(portfolio * last_price) - (portfolio * last_price if last_price > 0 else 0)],
    '% Unrealized P/L': [(portfolio * last_price / initial_investment * 100) if initial_investment else 0],
    'Realized P/L': [0],  # Update logic for realized profit
    'Maximum Drawdown': [0],  # Implement max drawdown logic
    '%Return': [(balance + portfolio * last_price - initial_investment) / initial_investment * 100],
}

summary_df = pd.DataFrame(summary_data)

# Save outputs
save_output(portfolio_df, "portfolio", team_name)
save_output(statement_df, "statement", team_name)
save_output(summary_df, "summary", team_name)



# portfolio_data['Table Name'].append('Portfolio_file')
# portfolio_data['File Name'].append(team_name)
# portfolio_data['Stock name'].append('AOT')
# portfolio_data['Start Vol'].append(0)
# portfolio_data['Actual Vol'].append(0)
# portfolio_data['Avg Cost'].append(0)
# portfolio_data['Market Price'].append(61.5)
# portfolio_data['Market Value'].append(0)
# portfolio_data['Amount Cost'].append(0)
# portfolio_data['Unrealized P/L'].append(0)
# portfolio_data['% Unrealized P/L'].append(0)
# portfolio_data['Realized P/L'].append(0)

# portfolio_df = pd.DataFrame(portfolio_data)

# statement_data['Table Name'].append('Statement_file')
# statement_data['File Name'].append(team_name)
# statement_data['Stock Name'].append('AOT')
# statement_data['Date'].append('2024-11-21')
# statement_data['Time'].append('09:56:23 AM')
# statement_data['Side'].append('Buy')
# statement_data['Volume'].append('100')
# statement_data['Price'].append('60.75')
# statement_data['Amount Cost'].append('6075')
# statement_data['End Line Available'].append(initial_balance)

# statement_df = pd.DataFrame(statement_data)

# last_end_line_available = 1
# count_win = 1
# count_sell = 1

# summary_data = {
#     'Table Name': ['Sum_file'],
#     'File Name': [team_name],
#     'trading_day': [1],  
#     'NAV': [portfolio_df['Market Value'].sum() + last_end_line_available],
#     'Portfolio value': [portfolio_df['Market Value'].sum()],
#     'End Line available': [last_end_line_available],  # Use the correct End Line Available
#     'Start Line available':[Start_Line_available],
#     'Number of wins': [count_win], 
#     'Number of matched trades': [count_sell], #นับ sell เพราะ เทรดbuy sellด้วย volume เท่ากัน
#     'Number of transactions:': [len(statement_df)],
#     'Net Amount': [statement_df['Amount Cost'].sum()],
#     'Unrealized P/L': [portfolio_df['Unrealized P/L'].sum()],
#     '% Unrealized P/L': [(portfolio_df['Unrealized P/L'].sum() / initial_investment * 100) if initial_investment else 0],
#     'Realized P/L': [portfolio_df['Realized P/L'].sum()],
#     'Maximum value': [statement_df['End Line Available'].max()],
#     'Minimum value': [statement_df['End Line Available'].min()],
#     'Win rate': [(count_win * 100)/ count_sell],
#     'Calmar Ratio': [((portfolio_df['Market Value'].sum() + last_end_line_available - initial_investment) / initial_investment * 100) / \
#                            ((portfolio_df['Market Value'].sum() + last_end_line_available - 10_000_000) / 10_000_000)],
#     'Relative Drawdown': [(portfolio_df['Market Value'].sum() + last_end_line_available - 10_000_000) / 10_000_000 / statement_df['End Line Available'].max() * 100],
#     'Maximum Drawdown': [(portfolio_df['Market Value'].sum() + last_end_line_available - 10_000_000) / 10_000_000],
#     '%Return': [((portfolio_df['Market Value'].sum() + last_end_line_available - initial_investment) / initial_investment * 100)]
# }

# summary_df = pd.DataFrame(summary_data)
# ################################################## End Ex Create and Save ##############################################################################

# save_output(portfolio_df, "portfolio", team_name)
# save_output(statement_df, "statement", team_name)
# save_output(summary_df, "summary", team_name)