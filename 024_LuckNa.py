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

file_path = os.path.expanduser('~/Desktop/Daily_Ticks_20241212.csv') 
df = pd.read_csv(file_path)

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
                print(f"Initial initial_balance (first value): {initial_balance}")
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
    print(f"Initial initial_balance = initial_investment: {initial_investment}")

stock_symbols = ["ADVANC", "AOT", "AWC", "BANPU", "BBL", "BCP", "BDMS", "BEM", "BGRIM", "BH",
    "BJC", "BTS", "CBG", "CENTEL", "COM7", "CPALL", "CPF", "CPN", "CRC", "DELTA",
    "EA", "EGCO", "GLOBAL", "GPSC", "GULF", "HMPRO", "INTUCH", "ITC", "IVL",
    "JMART", "JMT", "KBANK", "KTB", "KTC", "LH", "MINT", "MTC", "OR", "OSP", "PTT",
    "PTTEP", "PTTGC", "RATCH", "SAWAD", "SCB", "SCC", "SCGP", "TIDLOR", "TISCO",
    "TLI", "TOP", "TRUE", "TTB", "TU", "WHA"]


stock_dfs = df['ShareCode'].unique() # current stock
# change to numpy array
if prev_portfolio_df is not None:
    prev_act_dict = {}
    last_rows = prev_portfolio_df.groupby('Stock name')['Actual Vol'].last()
    prev_act_dict = dict(last_rows)
    
    for stock_df in stock_dfs:
        if stock_df not in prev_act_dict:
            prev_act_dict[stock_df] = 0
else:
    prev_act_dict = {stock : 0 for stock in stock_dfs}

    # for key, value in prev_act_dict.items():
        # print(f'{key} : {value}')

################################################################################################################################

# Calculate RSI using the 'LastPrice' column
rsi_period = 14
df['RSI'] = RSIIndicator(close=df['LastPrice'], window=rsi_period).rsi()

# Add trading conditions
buy_threshold = 30
sell_threshold = 70

# Initialize trading variables
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
    # 'Portfolio value' : [], #add
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

stock_totals = {stock: {'total_cost': 0, 'total_volume': 0, 'avg_cost': 0, 'Market Value' : 0} for stock in stock_dfs}
NAV = 0 
# Trading loop
for index, row in df.iterrows():
    stock_name = row['ShareCode']
    price = row['LastPrice']
    rsi = row['RSI']
    date_time = row['TradeDateTime']

    # Split date and time
    date = date_time.split()[0]
    time = date_time.split()[1]

    volume = np.random.choice(volume_options)
    # Buy condition
    if rsi < buy_threshold and initial_balance >= price * volume:
        cost = price * volume
        initial_balance -= cost
        last_price = price
        start_vol = int(prev_act_dict[stock_name]) #act_vol
        act_vol = start_vol + volume
        prev_act_dict[stock_name] = (act_vol)

        stock_totals[stock_name]['total_cost'] += price * volume
        stock_totals[stock_name]['total_volume'] += volume
        if stock_totals[stock_name]['total_volume'] == 0:
            stock_totals[stock_name]['avg_cost'] = 0
        else:  
            stock_totals[stock_name]['avg_cost'] = round(stock_totals[stock_name]['total_cost'] / stock_totals[stock_name]['total_volume'], 4)

        # # Update portfolio data for the buy
        # portfolio_data['Table Name'].append('Portfolio_file')
        # portfolio_data['File Name'].append(team_name)
        # portfolio_data['Stock name'].append(stock_name)
        # portfolio_data['Start Vol'].append(start_vol)
        # portfolio_data['Actual Vol'].append(prev_act_dict[stock_name])

        # portfolio_data['Avg Cost'].append(stock_totals[stock_name]['avg_cost'])
        # portfolio_data['Market Price'].append(price)
        # portfolio_data['Market Value'].append(act_vol * price)
        # portfolio_data['Amount Cost'].append(stock_totals[stock_name]['total_cost'])

        # unreal = (price - stock_totals[stock_name]['avg_cost']) * prev_act_dict[stock_name]
        # if stock_totals[stock_name]['avg_cost'] > 0:
        #     percent_unrealized_pl = ((price - stock_totals[stock_name]['avg_cost']) / stock_totals[stock_name]['avg_cost']) * 100
        # else:
        #     percent_unrealized_pl = 0  # Avoid division by zero
        # portfolio_data['Unrealized P/L'].append(unreal)
        # portfolio_data['% Unrealized P/L'].append(percent_unrealized_pl)
        # portfolio_data['Realized P/L'].append(0)  # No realized P/L for buy

        
        # Log the trade in the statement
        statement_data['Table Name'].append('Statement_file')
        statement_data['File Name'].append(team_name)
        statement_data['Stock Name'].append(stock_name)
        statement_data['Date'].append(date)
        statement_data['Time'].append(time)
        statement_data['Side'].append('Buy')
        statement_data['Volume'].append(volume)
        statement_data['Actual Vol'].append(prev_act_dict[stock_name])
        statement_data['Price'].append(price)
        statement_data['Amount Cost'].append(cost)
        statement_data['End Line available'].append(initial_balance)
        # statement_data['Portfolio value'].append() #add

        stock_totals[stock_name]['Market Value'] += act_vol * price
        statement_data['NAV'].append(float(stock_totals[stock_name]['Market Value']) + initial_balance)
    # Sell condition
    elif rsi > sell_threshold and act_vol > 0 and volume <= act_vol:
        revenue = price * act_vol
        initial_balance += revenue
        realized_pl = (price - last_price) * act_vol  # Profit from the sale
        start_vol = int(prev_act_dict[stock_name]) #act_vol
        act_vol = start_vol - volume
        prev_act_dict[stock_name] = (act_vol)

        stock_totals[stock_name]['total_cost'] -= price * volume
        stock_totals[stock_name]['total_volume'] -= volume
        if stock_totals[stock_name]['total_volume'] == 0:
            stock_totals[stock_name]['avg_cost'] = 0
        else:    
            stock_totals[stock_name]['avg_cost'] = round(stock_totals[stock_name]['total_cost'] / stock_totals[stock_name]['total_volume'], 4)
        
        # Update act_vol data for the sell
        # last row of stock
        # portfolio_data['Table Name'].append('Portfolio_file')
        # portfolio_data['File Name'].append(team_name)
        # portfolio_data['Stock name'].append(stock_name)
        # portfolio_data['Start Vol'].append(start_vol)
        # portfolio_data['Actual Vol'].append(prev_act_dict[stock_name])
        # portfolio_data['Avg Cost'].append(stock_totals[stock_name]['avg_cost'])
        # portfolio_data['Market Price'].append(price)
        # portfolio_data['Market Value'].append(act_vol * price)  # Market value after selling is 0
        # portfolio_data['Amount Cost'].append(stock_totals[stock_name]['total_cost'])  # No cost after selling

        # realized_pl = (price - stock_totals[stock_name]['avg_cost']) * prev_act_dict[stock_name]
        # # if stock_totals[stock_name]['avg_cost'] > 0:
        # #     percent_unrealized_pl = ((price - stock_totals[stock_name]['avg_cost']) / stock_totals[stock_name]['avg_cost']) * 100
        # # else:
        # #     percent_unrealized_pl = 0 
        # portfolio_data['Unrealized P/L'].append(0)
        # portfolio_data['% Unrealized P/L'].append(0)
        # portfolio_data['Realized P/L'].append(realized_pl)
        
        # Log the trade in the statement
        statement_data['Table Name'].append('Statement_file')
        statement_data['File Name'].append(team_name)
        statement_data['Stock Name'].append(stock_name)
        statement_data['Date'].append(date)
        statement_data['Time'].append(time)
        statement_data['Side'].append('Sell')
        statement_data['Volume'].append(volume)
        statement_data['Actual Vol'].append(prev_act_dict[stock_name]) 
        statement_data['Price'].append(price)
        statement_data['Amount Cost'].append(revenue)
        statement_data['End Line available'].append(initial_balance)
        # statement_data['Portfolio value'].append() #add
        stock_totals[stock_name]['Market Value'] += act_vol * price
        statement_data['NAV'].append(float(stock_totals[stock_name]['Market Value']) + initial_balance)


# portfolio_df = pd.DataFrame(portfolio_data)
statement_df = pd.DataFrame(statement_data)
save_output(statement_df, "statement", team_name)

# Create Portfolio
df_statement = pd.read_csv(os.path.expanduser("~/Desktop/competition_api/Result/statement/024_LuckNa_statement.csv"))
df_statement = df_statement.groupby('Stock Name').last()
# print(df_statement.loc[df_statement])
# print(df_statement['Stock Name']['AOT'])
# for stock_name in stock_totals:
#     portfolio_data['Table Name'].append('Portfolio_file')
#     portfolio_data['File Name'].append(team_name)
#     portfolio_data['Stock name'].append(stock_name)
#     portfolio_data['Start Vol'].append(int(prev_act_dict[stock_name]))
#     portfolio_data['Actual Vol'].append(prev_act_dict[stock_name])
#     # portfolio_data['Avg Cost'].append(stock_totals[stock_name]['avg_cost'])
#     # portfolio_data['Market Price'].append(price)
#     # portfolio_data['Market Value'].append(act_vol * price)  # Market value after selling is 0
#     # portfolio_data['Amount Cost'].append(stock_totals[stock_name]['total_cost'])  # No cost after selling
#     # realized_pl = (price - stock_totals[stock_name]['avg_cost']) * prev_act_dict[stock_name]
#     # # if stock_totals[stock_name]['avg_cost'] > 0:
#     # #     percent_unrealized_pl = ((price - stock_totals[stock_name]['avg_cost']) / stock_totals[stock_name]['avg_cost']) * 100
#     # # else:
#     # #     percent_unrealized_pl = 0 
#     # portfolio_data['Unrealized P/L'].append(0)
#     # portfolio_data['% Unrealized P/L'].append(0)
#     # portfolio_data['Realized P/L'].append(realized_pl)
#     # df_statement = df_statement.groupby('Stock name').last()
#     # prinmi)





# start_day  = datetime(2024, 12, 10)
# today  = datetime.now()

# last_end_line_available = initial_balance
# if statement_df is not None:
#     count_win = sum(1 for _, row in statement_df.iterrows() if row['Side'] == 'Sell' and row['Amount Cost'] > 0)
#     count_sell = len(statement_df[statement_df['Side'] == 'Sell'])
#     if count_sell == 0:
#         win_rate = prev_win_rate
#     else:
#         win_rate = (count_win * 100) / count_sell
# else:
#     count_win = 0
#     count_sell = 0
#     win_rate = 0

# summary_data = {
#     'Table Name': ['Sum_file'],
#     'File Name': [team_name],
#     'trading_day': [(today - start_day).days],  
#     'NAV': [portfolio_df['Market Value'].sum() + last_end_line_available],
#     'Portfolio value': [portfolio_df['Market Value'].sum()],
#     'End Line available': [last_end_line_available],
#     'Start Line available':[Start_Line_available],
#     'Number of wins': [count_win],
#     'Number of matched trades': [count_sell],
#     'Number of transactions': [len(statement_df)],
#     'Net Amount': [statement_df['Amount Cost'].sum()],
#     'Sum of Unrealized P/L': [portfolio_df['Unrealized P/L'].sum()],
#     'Sum of %Unrealized P/L': [(portfolio_df['Unrealized P/L'].sum() / initial_investment * 100) if initial_investment else 0],
#     'Sum of Realized P/L': [portfolio_df['Realized P/L'].sum()],
#     'Maximum value': [statement_df['End Line available'].max()],
#     'Minimum value': [statement_df['End Line available'].min()],
#     'Win rate': [win_rate],
#     'Calmar Ratio': [((portfolio_df['Market Value'].sum() + last_end_line_available - initial_investment) / initial_investment * 100) / \
#                            ((portfolio_df['Market Value'].sum() + last_end_line_available - 10_000_000) / 10_000_000)],
#     'Relative Drawdown': [(portfolio_df['Market Value'].sum() + last_end_line_available - 10_000_000) / 10_000_000 / statement_df['End Line available'].max() * 100],
#     'Maximum Drawdown': [(statement_df['End Line available'].min() - statement_df['End Line available'].max()) / statement_df['End Line available'].max() ],
#     '%Return': [((portfolio_df['Market Value'].sum() + last_end_line_available - initial_investment) / initial_investment * 100)]
# }


# summary_df = pd.DataFrame(summary_data)

# # Save outputs
# save_output(portfolio_df, "portfolio", team_name)
# # save_output(statement_df, "statement", team_name)
# save_output(summary_df, "summary", team_name)