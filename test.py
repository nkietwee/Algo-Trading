
import pandas as pd
import os

# # file_path = os.path.expanduser("/home/nkietwee/Desktop/competition_api/Result/summary/*.csv")
# file_path = os.path.expanduser("/home/nkietwee/Desktop/competition_api/Result/summary/024_LuckNa_summary.csv")
# file_path = os.path.expanduser("/home/nkietwee/Desktop/Daily_Ticks.csv")

# file_path = os.path.expanduser('/home/nkietwee/Desktop/competition_api/Result/portfolio/024_LuckNa_portfolio.csv') 
# file_path = os.path.expanduser('/home/nkietwee/Desktop/competition_api/Result/statement/024_LuckNa_statement.csv') 
# file_path = os.path.expanduser('/home/nkietwee/Desktop/competition_api/Result/summary/024_LuckNa_summary.csv') 

# df = len(df['Stock name'].unique())
# df = pd.read_csv(file_path)

# df = df[df['Actual Vol'] < 0]
# df = df.tail()

# print(df.head(100))
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

# # df = pd.read_csv("/home/nkietwee/Desktop/competition_api_new/Previous/summary/024_LuckNa_summary.csv")
# df = pd.read_csv("/home/nkietwee/Desktop/competition_api/Result/portfolio/024_LuckNa_portfolio.csv")
# print(df.head(20))

# def cnt_stock(stock_name):
#     stock_symbols = ["ADVANC","AOT","AWC","BBL", "BCP", "BDMS", "BEM", "BGRIM", "BH", "BJC",
#                   "BTS", "CBG", "CENTEL", "CPALL", "CPF", "CPN", "CRC", "DELTA", "EA", "EGCO",
#                   "GLOBAL", "GPSC", "GULF", "HMPRO", "INTUCH", "ITC", "IVL", "KBANK", "KTB",
#                   "KTC", "LH", "MINT", "MTC", "OR", "OSP", "PTT", "PTTEP", "PTTGC", "RATCH",
#                   "SCB", "SCC", "SCGP", "TIDLOR", "TISCO", "TLI", "TOP", "TRUE", "TTB", "TU", "WHA" ]
#     cnt = []
#     if stock_name in stock_symbols:
#         cnt

# def cnt_stock(stock_name, start, amount):
#     stock_symbols = ["ADVANC","AOT","AWC","BBL", "BCP", "BDMS", "BEM", "BGRIM", "BH", "BJC",
#                   "BTS", "CBG", "CENTEL", "CPALL", "CPF", "CPN", "CRC", "DELTA", "EA", "EGCO",
#                   "GLOBAL", "GPSC", "GULF", "HMPRO", "INTUCH", "ITC", "IVL", "KBANK", "KTB",
#                   "KTC", "LH", "MINT", "MTC", "OR", "OSP", "PTT", "PTTEP", "PTTGC", "RATCH",
#                   "SCB", "SCC", "SCGP", "TIDLOR", "TISCO", "TLI", "TOP", "TRUE", "TTB", "TU", "WHA"]
#     cnt = [0] * 50
#     print(f'len : {len(stock_symbols)}')
#     print(f'cnt : {len(cnt)}')
#     for i in range(len(stock_symbols)):
#         if stock_name == stock_symbols[i]:
#             print(f'i : {i}')
#             cnt.insert(i, start + amount)
#             break
#     return cnt

# lst = cnt_stock("WHA", 0 , 400)
# print(lst)

# import pandas as pd

# # df = pd.DataFrame({'date': ['2022-06-01 12:00:00', '2022-06-02 13:00:00', '2022-06-03 14:00:00']})
# df = pd.DataFrame({'date' : ['2024-12-18 09:55:51']})
# # convert the date column to datetime format
# # print(type(df))
# df['date'] = pd.to_datetime(df['date'])

# # change the datetime format
# # df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
# # df['date'] = pd.to_datetime(df['date'],  format='%Y-%m-%d %H:%M:%S.%f').dt.time

# # print(type(df['date'][0]))
# date = df['date'].date
# timee = df['date'].time
# print(date)
# print(timee)

# file_path = os.path.expanduser("/home/nkietwee/Desktop/competition_api/Result/summary/*.csv")
# file_path = os.path.expanduser("/home/nkietwee/Desktop/competition_api/Result/summary/024_LuckNa_summary.csv")
# file_path = os.path.expanduser("/home/nkietwee/Desktop/Daily_Ticks.csv")

# file_path = os.path.expanduser('/home/nkietwee/Desktop/competition_api/Result/portfolio/024_LuckNa_portfolio.csv') 
# file_path = os.path.expanduser('/home/nkietwee/Desktop/competition_api/Result/statement/024_LuckNa_statement.csv') 
# file_path = os.path.expanduser('/home/nkietwee/Desktop/competition_api/Result/summary/024_LuckNa_summary.csv') 

# df = pd.read_csv(file_path)

# df = df[df['Actual Vol'] < 0]
# df = df.tail()

# print(df.head(100))

# import pandas as pd

# # create a DataFrame with datetime data
# df = pd.DataFrame({'date': ['2022-06-01 12:00:00', '2022-06-02 13:00:00', '2022-06-03 14:00:00']})

# # convert the date column to datetime format
# df['date'] = pd.to_datetime(df['date'])

# # change the datetime format
# df['date'] = df['date'].dt.strftime('%Y/%m/%d %H:%M:%S')

# print(type(df['date'][0]))
# print(df)
from datetime import datetime, timedelta
from datetime import time

start_day  = datetime(2024, 12, 23)
# today  = datetime.now()
today  = datetime(2025, 1, 10)

day_no = 0
tmp_day = (today - start_day).days
print(f'tmp_day : {tmp_day}')
if (tmp_day >= 7 and tmp_day <= 11):
    day_no = tmp_day - 2
elif tmp_day >= 14 and tmp_day <= 18:
    day_no = tmp_day - 4

print(day_no)
exit(0)
# print(f'day : {(today - start_day).days}')
# 10 มกราคม 2568
start_day  = datetime(2024, 12, 23)
end_date = datetime(2025, 1, 10)
today  = datetime.now()
day_no = (today - start_day).days

delta = timedelta(days=1)
while (today <= end_date):
    if (today.weekday() > 4):
       print(today.strftime("%A"))
    today += delta

# print(delta)