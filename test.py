
import pandas as pd
import os

# file_path = os.path.expanduser("/home/nkietwee/Desktop/competition_api/Result/summary/*.csv")
# file_path = os.path.expanduser("/home/nkietwee/Desktop/competition_api/Result/summary/024_LuckNa_summary.csv")
file_path = os.path.expanduser("/home/nkietwee/Desktop/Daily_Ticks.csv")
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    print(df)
    # print(data['TradeDateTime'])
    # print(pd.to_datetime(data['TradeDateTime']))
    # df['TradeDateTime'] = pd.to_datetime(df['TradeDateTime'])

# Sort data by datetime (important for chronological simulation)
    # df = df.sort_values(by='TradeDateTime')
    # print(df)
else:
    print("Don't have")
# print("finish")
# print(file_path)