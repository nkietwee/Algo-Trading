import pandas as pd
import numpy as np
import os
from datetime import datetime
from datetime import time
from ta.momentum import RSIIndicator

################################################################################################################################

team_name = '024_LuckNa'

################################################################################################################################

output_dir = os.path.expanduser("~/Desktop/competition_api")
if not os.path.exists(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    print(f"Created main directory: {output_dir}")

def load_previous(file_type, teamName):
    output_dir = os.path.expanduser("~/Desktop/competition_api")
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

statements = []

file_path = os.path.expanduser('~/Desktop/Daily_Ticks.csv') 
# file_path = os.path.expanduser('~/Desktop/Daily_Ticks_20241217.csv') 
# file_path = os.path.expanduser('~/Desktop/Daily_Ticks_18.csv')

df = pd.read_csv(file_path)

# sort value
df['TradeDateTime'] = pd.to_datetime(df['TradeDateTime'])
# print(df.head())
# exit(0)
df = df.sort_values(by='TradeDateTime')
initial_investment = 10000000

# Load the prev file
prev_summary_df = load_previous("summary", team_name)
# prev_statement_df = load_previous("statement", team_name)
prev_portfolio_df = load_previous("portfolio", team_name)

if prev_summary_df is not None:
    if 'End Line available' in prev_summary_df.columns:
        # ดึงค่าคอลัมน์ 'End Line available' ทั้งหมด
        initial_balance_series = prev_summary_df['End Line available']
        # print(f'initial_balance_series : {initial_balance_series}')
        # ตรวจสอบว่าคอลัมน์ไม่ว่างเปล่า
        if not initial_balance_series.empty:
            # เข้าถึงค่าแรกของคอลัมน์
            first_value = initial_balance_series.iloc[0]
            
            # ลบเครื่องหมายคั่นหลักพันและแปลงเป็น float
            try:
                initial_balance = float(str(first_value).replace(',', '').strip())
                Start_Line_available = initial_balance
                prev_win_rate = prev_summary_df['Win rate'][0]
                # print(f'pre_win_rate : {prev_win_rate}')
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
    prev_win_rate = 0
    print(f"Initial balance = initial_investment: {initial_investment}")

stock_dfs = df['ShareCode'].unique() # current stock
# change to numpy array
if prev_portfolio_df is not None:
    prev_act_dict = {}
    start_dict = {}
    last_rows = prev_portfolio_df.groupby('Stock name')['Actual Vol'].last()
    prev_act_dict = dict(last_rows)
    start_dict = dict(last_rows)
    
    for stock_df in stock_dfs:
        if stock_df not in prev_act_dict:
            prev_act_dict[stock_df] = 0
            start_dict[stock_df] = 0
else: #in case don't have portfolio
    prev_act_dict = {stock : 0 for stock in stock_dfs}
    start_dict = {stock : 0 for stock in stock_dfs}
    # for key, value in prev_act_dict.items():
        # print(f'{key} : {value}')

################################################################################################################################

# Calculate RSI using the 'LastPrice' column
rsi_period = 14
df['RSI'] = RSIIndicator(close=df['LastPrice'], window=rsi_period).rsi()

# Add trading conditions
buy_threshold = 30
sell_threshold = 70

# Initialize trading variable
initial_balance = initial_investment
act_vol = 0  # Shares held
start_vol = 0
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
    'Amount Cost': [],
    'Market Value': [],
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
    'Actual Vol' : [],
    'Price': [],
    'Amount Cost': [],
    'End Line available' : [],
    'Portfolio value' : [],
    'NAV' : []
}

summary_data = {
    'Table Name': [],
    'File Name': [],
    'NAV': [],
    'End Line available': [],
    'Start Line available': [],
    'Number of wins': [], 
    'Number of matched trades': [],
    'Number of transactions:': [],
    'Sum of Unrealized P/L': [],
    'Sum of %Unrealized P/L':[],
    'Sum of Realized P/L': [],
    'Maximum value': [],
    'Minimum value': [],
    'Win rate': [],
    'Calmar Ratio': [],
    'Relative Drawdown': [],
    'Maximum Drawdown': [],
    '%Return': []
}

# List of variable trading volumes
volume_options = [100, 200, 300, 500]

stock_totals = {stock: {'total_cost': 0, 'total_volume': 0, 'avg_cost': 0, 'Market Value' : 0, 'sell_volume' : 0} for stock in stock_dfs}

# Trading loop
for index, row in df.iterrows():
    stock_name = row['ShareCode']
    price = row['LastPrice']
    rsi = row['RSI']
    date_time = row['TradeDateTime']

    date = date_time.date()
    timee = date_time.time()

    volume = np.random.choice(volume_options)
    # volume = 100

    # Buy condition
    # if rsi < buy_threshold and initial_balance >= price * volume and stock_totals[stock_name]['buy_state'] == 0:
    if rsi < buy_threshold and initial_balance >= price * volume:
        cost = price * volume
        initial_balance -= cost
        last_price = price
        start_vol = int(prev_act_dict[stock_name]) #act_vol
        act_vol = start_vol + volume
        prev_act_dict[stock_name] = (act_vol)

        stock_totals[stock_name]['total_cost'] += cost
        stock_totals[stock_name]['total_volume'] += volume
        if stock_totals[stock_name]['total_volume'] == 0:
            stock_totals[stock_name]['avg_cost'] = 0
        else:  
            stock_totals[stock_name]['avg_cost'] = round(stock_totals[stock_name]['total_cost'] / stock_totals[stock_name]['total_volume'], 4)

        # Log the trade in the statement
        statement_data['Table Name'].append('Statement_file')
        statement_data['File Name'].append(team_name)
        statement_data['Stock Name'].append(stock_name)
        statement_data['Date'].append(date)
        statement_data['Time'].append(timee)
        statement_data['Side'].append('Buy')
        statement_data['Volume'].append(volume)
        statement_data['Actual Vol'].append(prev_act_dict[stock_name])
        statement_data['Price'].append(price)
        statement_data['Amount Cost'].append(cost)
        statement_data['End Line available'].append(initial_balance)
        
        # for use in portfolio
        stock_totals[stock_name]['Market Value'] += act_vol * price

        statement_data['Portfolio value'].append(stock_totals[stock_name]['Market Value'])
        statement_data['NAV'].append(float(stock_totals[stock_name]['Market Value']) + initial_balance)
    # Sell condition
    # Don't forget to cut loss
    elif rsi > sell_threshold and prev_act_dict[stock_name] > 0 and volume <= prev_act_dict[stock_name]:
        revenue = price * volume
        initial_balance += revenue
        start_vol = int(prev_act_dict[stock_name]) #act_vol
        act_vol = start_vol - volume
        prev_act_dict[stock_name] = (act_vol)

        stock_totals[stock_name]['total_cost'] -= volume * stock_totals[stock_name]['avg_cost']
        stock_totals[stock_name]['total_volume'] -= volume
        if stock_totals[stock_name]['total_volume'] == 0:
            stock_totals[stock_name]['avg_cost'] = 0
        else:    
            stock_totals[stock_name]['avg_cost'] = round(stock_totals[stock_name]['total_cost'] / stock_totals[stock_name]['total_volume'], 4)
        
        # Log the trade in the statement
        statement_data['Table Name'].append('Statement_file')
        statement_data['File Name'].append(team_name)
        statement_data['Stock Name'].append(stock_name)
        statement_data['Date'].append(date)
        statement_data['Time'].append(timee)
        statement_data['Side'].append('Sell')
        statement_data['Volume'].append(volume)
        statement_data['Actual Vol'].append(prev_act_dict[stock_name]) 
        statement_data['Price'].append(price)
        statement_data['Amount Cost'].append(revenue)
        statement_data['End Line available'].append(initial_balance)

        stock_totals[stock_name]['Market Value'] += act_vol * price
        stock_totals[stock_name]['sell_volume'] += volume
        
        statement_data['Portfolio value'].append(stock_totals[stock_name]['Market Value'])
        statement_data['NAV'].append(float(stock_totals[stock_name]['Market Value']) + initial_balance)

    if initial_balance <= 2500000:
        # print("keep money")
        break


statement_df = pd.DataFrame(statement_data)

# Create Portfolio
statement_lastrows = statement_df.groupby('Stock Name').last()
df_stock = statement_lastrows.index.tolist()

for stock_name in df_stock:
    if statement_lastrows['Actual Vol'][stock_name] != 0 :
        portfolio_data['Table Name'].append('Portfolio_file')
        portfolio_data['File Name'].append(team_name)
        portfolio_data['Stock name'].append(stock_name)
        portfolio_data['Start Vol'].append(int(start_dict[stock_name]))
        portfolio_data['Actual Vol'].append(statement_lastrows['Actual Vol'][stock_name])
        portfolio_data['Avg Cost'].append(stock_totals[stock_name]['avg_cost'])
        portfolio_data['Market Price'].append(statement_lastrows['Price'][stock_name])
        portfolio_data['Market Value'].append(statement_lastrows['Price'][stock_name] * statement_lastrows['Actual Vol'][stock_name])  # Market value after selling is 0
        portfolio_data['Amount Cost'].append(round(stock_totals[stock_name]['total_cost'], 4))  # No cost after selling
        realized_pl = (price - stock_totals[stock_name]['avg_cost']) * prev_act_dict[stock_name]
        
        unreal =  portfolio_data['Market Value'][-1] - stock_totals[stock_name]['total_cost'] # current - buy
        if stock_totals[stock_name]['total_cost'] == 0:
            percent_unrealized_pl = 0
        else:
            percent_unrealized_pl = (unreal / stock_totals[stock_name]['total_cost']) * 100

        if stock_totals[stock_name]['sell_volume'] == 0:
            realized_pl = 0
        else:
            realized_pl =  portfolio_data['Market Value'][-1] - (stock_totals[stock_name]['sell_volume'] * stock_totals[stock_name]['avg_cost'])

        portfolio_data['Unrealized P/L'].append(unreal)
        portfolio_data['% Unrealized P/L'].append(percent_unrealized_pl)
        portfolio_data['Realized P/L'].append(realized_pl)

portfolio_df = pd.DataFrame(portfolio_data)


last_end_line_available = initial_balance
if statement_df is not None:
    count_win = sum(1 for _, row in statement_df.iterrows() if row['Side'] == 'Sell' and row['Amount Cost'] > 0)
    count_sell = len(statement_df[statement_df['Side'] == 'Sell'])
    if count_sell == 0:
        win_rate = prev_win_rate
    else:
        win_rate = (count_win * 100) / count_sell
else:
    count_win = 0
    count_sell = 0
    win_rate = 0

def getday():
    start_day  = datetime(2024, 12, 23)
    # today  = datetime(2025, 1, 9)
    today  = datetime.now()
    tmp_day = (today - start_day).days
    day_no = 0
    if (tmp_day < 7):
        day_no = tmp_day
    elif (tmp_day >= 7 and tmp_day <= 11):
        day_no = tmp_day - 2
    elif tmp_day >= 14 and tmp_day <= 18:
        day_no = tmp_day - 4
    return (day_no)

summary_data = {
    'Table Name': ['Sum_file'],
    'File Name': [team_name],
    'trading_day': [getday()],  
    'NAV': [portfolio_df['Market Value'].sum() + last_end_line_available],
    'Portfolio value': [portfolio_df['Market Value'].sum()],
    'End Line available': [last_end_line_available],
    'Start Line available':[Start_Line_available],
    'Number of wins': [count_win],
    'Number of matched trades': [count_sell],
    'Number of transactions': [len(statement_df)],
    'Net Amount': [statement_df['Amount Cost'].sum()],
    'Sum of Unrealized P/L': [portfolio_df['Unrealized P/L'].sum()],
    'Sum of %Unrealized P/L': [(portfolio_df['Unrealized P/L'].sum() / initial_investment * 100) if initial_investment else 0],
    'Sum of Realized P/L': [portfolio_df['Realized P/L'].sum()],
    'Maximum value': [statement_df['End Line available'].max()],
    'Minimum value': [statement_df['End Line available'].min()],
    'Win rate': [win_rate],
    'Calmar Ratio': [((portfolio_df['Market Value'].sum() + last_end_line_available - initial_investment) / initial_investment * 100) / \
                           ((portfolio_df['Market Value'].sum() + last_end_line_available - 10_000_000) / 10_000_000)],
    'Relative Drawdown': [(portfolio_df['Market Value'].sum() + last_end_line_available - 10_000_000) / 10_000_000 / statement_df['End Line available'].max() * 100],
    'Maximum Drawdown': [(statement_df['End Line available'].min() - statement_df['End Line available'].max()) / statement_df['End Line available'].max() ],
    '%Return': [((portfolio_df['Market Value'].sum() + last_end_line_available - initial_investment) / initial_investment * 100)]
}

# Maximum Drawdown = ((Minimum Value − Maximum Value) / Maximum Value)*100
summary_df = pd.DataFrame(summary_data)

# # Save outputs
save_output(portfolio_df, "portfolio", team_name)
save_output(statement_df, "statement", team_name)
save_output(summary_df, "summary", team_name)