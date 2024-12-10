import pandas as pd
import numpy as np
import os
from datetime import datetime

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

# Function to calculate RSI
def calculate_rsi(data, window):
    delta = data['LastPrice'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=window).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Load historical data
file_path = '~/Desktop/Daily_Ticks.csv'
df = pd.read_csv(file_path)

initial_investment = 10000000

# Load the summary file
prev_summary_df = load_previous("summary", team_name)

if prev_summary_df is not None:
    if 'End Line available' in prev_summary_df.columns:
        initial_balance_series = prev_summary_df['End Line available']
        if not initial_balance_series.empty:
            try:
                initial_balance = float(str(initial_balance_series.iloc[0]).replace(',', '').strip())
                Start_Line_available = initial_balance
            except ValueError:
                initial_balance = initial_investment
        else:
            initial_balance = initial_investment
    else:
        initial_balance = initial_investment
else:
    initial_balance = initial_investment
    Start_Line_available = initial_investment

# Calculate RSI
rsi_window = 14
df['RSI'] = calculate_rsi(df, rsi_window)

# Define buy/sell signals based on RSI
df['Signal'] = 0
df.loc[df['RSI'] < 30, 'Signal'] = 1  # Buy signal (oversold)
df.loc[df['RSI'] > 70, 'Signal'] = -1  # Sell signal (overbought)

################################################################################################################################

# Initialize trading simulation variables
cash = initial_balance
position = 0
portfolio_data = []
statement_data = []
summary_data = []

# Simulate trades
for index, row in df.iterrows():
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
    if row['Signal'] == 1 and cash >= row['LastPrice'] * 100:  # Buy signal
        volume = 100
        cost = volume * row['LastPrice']
        cash -= cost
        position += volume
        # Log a trade
        statement_data['Table Name'].append('Statement_file')
        statement_data['File Name'].append(team_name)
        statement_data['Stock Name'].append(row['ShareCode'])
        statement_data['Date'].append(row['TradeDateTime'].split(' ')[0])
        statement_data['Time'].append(row['TradeDateTime'].split(' ')[1])
        statement_data['Side'].append('B' if row['Signal'] == 1 else 'S')
        statement_data['Volume'].append(volume)
        statement_data['Price'].append(row['LastPrice'])
        statement_data['Amount Cost'].append(volume * row['LastPrice'])
        statement_data['End Line Available'].append(cash)

    elif row['Signal'] == -1 and position > 0:  # Sell signal
        volume = 100
        revenue = volume * row['LastPrice']
        cash += revenue
        position -= volume
        # Log a trade
        statement_data['Table Name'].append('Statement_file')
        statement_data['File Name'].append(team_name)
        statement_data['Stock Name'].append(row['ShareCode'])
        statement_data['Date'].append(row['TradeDateTime'].split(' ')[0])
        statement_data['Time'].append(row['TradeDateTime'].split(' ')[1])
        statement_data['Side'].append('B' if row['Signal'] == 1 else 'S')
        statement_data['Volume'].append(volume)
        statement_data['Price'].append(row['LastPrice'])
        statement_data['Amount Cost'].append(volume * row['LastPrice'])
        statement_data['End Line Available'].append(cash)

    # Track portfolio data
    # Update after each trade
    portfolio_data['Table Name'].append('Portfolio_file')
    portfolio_data['File Name'].append(team_name)
    portfolio_data['Stock name'].append(row['ShareCode'])
    portfolio_data['Start Vol'].append(position)
    portfolio_data['Actual Vol'].append(position)
    portfolio_data['Avg Cost'].append(avg_cost if position > 0 else 0)
    portfolio_data['Market Price'].append(row['LastPrice'])
    portfolio_data['Market Value'].append(position * row['LastPrice'])
    portfolio_data['Amount Cost'].append(position * avg_cost)
    unrealized_pl = (position * row['LastPrice']) - (position * avg_cost)
    portfolio_data['Unrealized P/L'].append(unrealized_pl)
    portfolio_data['% Unrealized P/L'].append((unrealized_pl / (position * avg_cost)) * 100 if position > 0 else 0)
    portfolio_data['Realized P/L'].append(realized_pl)

# Summarize results
final_nav = cash + (position * df.iloc[-1]['LastPrice'])
summary_data = {
    'Table Name': ['Sum_file'],
    'File Name': [team_name],
    'trading_day': [1],
    'NAV': [cash + (position * df.iloc[-1]['LastPrice'])],
    'Portfolio value': [position * df.iloc[-1]['LastPrice']],
    'End Line available': [cash],
    'Number of wins': [win_count],
    'Number of matched trades': [trade_count],
    'Number of transactions:': [len(statement_data['Side'])],
    'Net Amount': [cash],
    'Unrealized P/L': [sum(portfolio_data['Unrealized P/L'])],
    '% Unrealized P/L': [(sum(portfolio_data['Unrealized P/L']) / initial_investment) * 100],
    'Realized P/L': [realized_pl],
    'Maximum value': [max(portfolio_data['Market Value'])],
    'Minimum value': [min(portfolio_data['Market Value'])],
    'Win rate': [(win_count / trade_count) * 100 if trade_count > 0 else 0],
    'Calmar Ratio': [(realized_pl / abs(max_drawdown)) if max_drawdown < 0 else 0],
    'Relative Drawdown': [(cash - min(portfolio_data['Market Value'])) / initial_investment],
    'Maximum Drawdown': [max_drawdown],
    '%Return': [(cash + (position * df.iloc[-1]['LastPrice']) - initial_investment) / initial_investment * 100]
}


# Convert to DataFrame
portfolio_df = pd.DataFrame(portfolio_data)
statement_df = pd.DataFrame(statement_data)
summary_df = pd.DataFrame(summary_data)

# Save results
save_output(portfolio_df, "portfolio", team_name)
save_output(statement_df, "statement", team_name)
save_output(summary_df, "summary", team_name)
