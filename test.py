
import pandas as pd
import os

# # file_path = os.path.expanduser("/home/nkietwee/Desktop/competition_api/Result/summary/*.csv")
# # file_path = os.path.expanduser("/home/nkietwee/Desktop/competition_api/Result/summary/024_LuckNa_summary.csv")
# # file_path = os.path.expanduser("/home/nkietwee/Desktop/Daily_Ticks.csv")

# file_path = os.path.expanduser('~/Desktop/Daily_Ticks.csv') 
# df = pd.read_csv(file_path)

# if os.path.exists(file_path):
#     df = pd.read_csv(file_path)
#     print(df)
#     # print(data['TradeDateTime'])
#     # print(pd.to_datetime(data['TradeDateTime']))
#     # df['TradeDateTime'] = pd.to_datetime(df['TradeDateTime'])

# # Sort data by datetime (important for chronological simulation)
#     # df = df.sort_values(by='TradeDateTime')
#     # print(df)
# else:
#     print("Don't have")
# # print("finish")
# # print(file_path)
# volume_options = [100, 200, 300, 500]
# df = pd.read_csv("/home/nkietwee/Desktop/competition_api_new/Result/statement/024_LuckNa_statement.csv")
# # df[df['Volume'].isin(volume_options)]
# cnt = 0
# for i in df['Side']:
#     if i == "Buy":
#         cnt += 1
#         # print(i)
#     else:
#         print(i)
# print(f'cnt : {cnt}')
# from datetime import date, datetime

# # start  = date(2024, 12, 12)
# start  = datetime(2024, 11, 30)
# end  = datetime.now()
# # print(end)
# print((end - start).days)

# import pandas as pd

# df = pd.read_csv("/home/nkietwee/Desktop/competition_api_new/Previous/summary/024_LuckNa_summary.csv")
# print(df)