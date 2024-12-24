
# import pandas as pd
# import os

# file_path = os.path.expanduser("/home/nkietwee/Desktop/competition_api/Previous/summary/024_LuckNa_summary.csv")

# df = pd.read_csv(file_path)
# print(len(df))
# # # file_path = os.path.expanduser("/home/nkietwee/Desktop/competition_api/Result/summary/*.csv")
# file_path = os.path.expanduser("/home/nkietwee/Desktop/competition_api/Result/summary/024_LuckNa_summary.csv")
# # file_path = os.path.expanduser("/home/nkietwee/Desktop/Daily_Ticks.csv")

# # file_path = os.path.expanduser('/home/nkietwee/Desktop/competition_api/Result/portfolio/024_LuckNa_portfolio.csv') 
# # file_path = os.path.expanduser('/home/nkietwee/Desktop/competition_api/Result/statement/024_LuckNa_statement.csv') 
# # # file_path = os.path.expanduser('/home/nkietwee/Desktop/competition_api/Result/summary/024_LuckNa_summary.csv') 

# # # df = len(df['Stock name'].unique())
# # df = pd.read_csv(file_path)
# # df = df.groupby('Stock Name').first()
# # df.to_csv("/home/nkietwee/Desktop/tmp.csv")
# # # df = df[df['Actual Vol'] < 0]
# # # df = df.tail()

# # print(df)
# # if os.path.exists(file_path):
# #     df = pd.read_csv(file_path)
# #     print(df)
# #     # print(data['TradeDateTime'])
# #     # print(pd.to_datetime(data['TradeDateTime']))
# #     # df['TradeDateTime'] = pd.to_datetime(df['TradeDateTime'])

# # # Sort data by datetime (important for chronological simulation)
# #     # df = df.sort_values(by='TradeDateTime')
# #     # print(df)
# # else:
# #     print("Don't have")
# # # print("finish")
# # # print(file_path)
# # volume_options = [100, 200, 300, 500]
# # df = pd.read_csv("/home/nkietwee/Desktop/competition_api_new/Result/statement/024_LuckNa_statement.csv")
# # # df[df['Volume'].isin(volume_options)]
# # cnt = 0
# # for i in df['Side']:
# #     if i == "Buy":
# #         cnt += 1
# #         # print(i)
# #     else:
# #         print(i)
# # print(f'cnt : {cnt}')
# # from datetime import date, datetime

# # # start  = date(2024, 12, 12)
# # start  = datetime(2024, 11, 30)
# # end  = datetime.now()
# # # print(end)
# # print((end - start).days)

# # import pandas as pd

# # # df = pd.read_csv("/home/nkietwee/Desktop/competition_api_new/Previous/summary/024_LuckNa_summary.csv")
# # df = pd.read_csv("/home/nkietwee/Desktop/competition_api/Result/portfolio/024_LuckNa_portfolio.csv")
# # print(df.head(20))

# # def cnt_stock(stock_name):
# #     stock_symbols = ["ADVANC","AOT","AWC","BBL", "BCP", "BDMS", "BEM", "BGRIM", "BH", "BJC",
# #                   "BTS", "CBG", "CENTEL", "CPALL", "CPF", "CPN", "CRC", "DELTA", "EA", "EGCO",
# #                   "GLOBAL", "GPSC", "GULF", "HMPRO", "INTUCH", "ITC", "IVL", "KBANK", "KTB",
# #                   "KTC", "LH", "MINT", "MTC", "OR", "OSP", "PTT", "PTTEP", "PTTGC", "RATCH",
# #                   "SCB", "SCC", "SCGP", "TIDLOR", "TISCO", "TLI", "TOP", "TRUE", "TTB", "TU", "WHA" ]
# #     cnt = []
# #     if stock_name in stock_symbols:
# #         cnt

# # def cnt_stock(stock_name, start, amount):
# #     stock_symbols = ["ADVANC","AOT","AWC","BBL", "BCP", "BDMS", "BEM", "BGRIM", "BH", "BJC",
# #                   "BTS", "CBG", "CENTEL", "CPALL", "CPF", "CPN", "CRC", "DELTA", "EA", "EGCO",
# #                   "GLOBAL", "GPSC", "GULF", "HMPRO", "INTUCH", "ITC", "IVL", "KBANK", "KTB",
# #                   "KTC", "LH", "MINT", "MTC", "OR", "OSP", "PTT", "PTTEP", "PTTGC", "RATCH",
# #                   "SCB", "SCC", "SCGP", "TIDLOR", "TISCO", "TLI", "TOP", "TRUE", "TTB", "TU", "WHA"]
# #     cnt = [0] * 50
# #     print(f'len : {len(stock_symbols)}')
# #     print(f'cnt : {len(cnt)}')
# #     for i in range(len(stock_symbols)):
# #         if stock_name == stock_symbols[i]:
# #             print(f'i : {i}')
# #             cnt.insert(i, start + amount)
# #             break
# #     return cnt

# # lst = cnt_stock("WHA", 0 , 400)
# # print(lst)

# # import pandas as pd

# # # df = pd.DataFrame({'date': ['2022-06-01 12:00:00', '2022-06-02 13:00:00', '2022-06-03 14:00:00']})
# # df = pd.DataFrame({'date' : ['2024-12-18 09:55:51']})
# # # convert the date column to datetime format
# # # print(type(df))
# # df['date'] = pd.to_datetime(df['date'])

# # # change the datetime format
# # # df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
# # # df['date'] = pd.to_datetime(df['date'],  format='%Y-%m-%d %H:%M:%S.%f').dt.time

# # # print(type(df['date'][0]))
# # date = df['date'].date
# # timee = df['date'].time
# # print(date)
# # print(timee)

# # file_path = os.path.expanduser("/home/nkietwee/Desktop/competition_api/Result/summary/*.csv")
# # file_path = os.path.expanduser("/home/nkietwee/Desktop/competition_api/Result/summary/024_LuckNa_summary.csv")
# # file_path = os.path.expanduser("/home/nkietwee/Desktop/Daily_Ticks.csv")

# # file_path = os.path.expanduser('/home/nkietwee/Desktop/competition_api/Result/portfolio/024_LuckNa_portfolio.csv') 
# # file_path = os.path.expanduser('/home/nkietwee/Desktop/competition_api/Result/statement/024_LuckNa_statement.csv') 
# # file_path = os.path.expanduser('/home/nkietwee/Desktop/competition_api/Result/summary/024_LuckNa_summary.csv') 

# # df = pd.read_csv(file_path)

# # df = df[df['Actual Vol'] < 0]
# # df = df.tail()

# # print(df.head(100))

# # import pandas as pd

# # # create a DataFrame with datetime data
# # df = pd.DataFrame({'date': ['2022-06-01 12:00:00', '2022-06-02 13:00:00', '2022-06-03 14:00:00']})

# # # convert the date column to datetime format
# # df['date'] = pd.to_datetime(df['date'])

# # # change the datetime format
# # df['date'] = df['date'].dt.strftime('%Y/%m/%d %H:%M:%S')

# # print(type(df['date'][0]))
# # print(df)
# # from datetime import datetime, timedelta
# # from datetime import time

# # start_day  = datetime(2024, 12, 23)
# # # today  = datetime.now()
# # today  = datetime(2025, 1, 10)

# # day_no = 0
# # tmp_day = (today - start_day).days
# # print(f'tmp_day : {tmp_day}')
# # if (tmp_day >= 7 and tmp_day <= 11):
# #     day_no = tmp_day - 2
# # elif tmp_day >= 14 and tmp_day <= 18:
# #     day_no = tmp_day - 4

# # print(day_no)
# # exit(0)
# # # print(f'day : {(today - start_day).days}')
# # # 10 มกราคม 2568
# # start_day  = datetime(2024, 12, 23)
# # end_date = datetime(2025, 1, 10)
# # today  = datetime.now()
# # day_no = (today - start_day).days

# # delta = timedelta(days=1)
# # while (today <= end_date):
# #     if (today.weekday() > 4):
# #        print(today.strftime("%A"))
# #     today += delta

# # print(delta)

# # import pandas as pd

# # # Provided data as a dictionary
# # data = {
# #     'ADVANC': {'total_cost': 0, 'total_volume': 0, 'avg_cost': 0, 'Market Value': 0, 'sell_volume': 0},
# #     'RATCH': {'total_cost': 63100.0, 'total_volume': 2000, 'avg_cost': 31.55, 'Market Value': 63000.0, 'sell_volume': 0},
# #     'SAWAD': {'total_cost': 122173.9, 'total_volume': 3000, 'avg_cost': 40.7246, 'Market Value': 126000.0, 'sell_volume': 2400},
# #     'BH': {'total_cost': 0, 'total_volume': 0, 'avg_cost': 0, 'Market Value': 0, 'sell_volume': 0},
# #     'SCB': {'total_cost': 11750.0, 'total_volume': 100, 'avg_cost': 117.5, 'Market Value': 11750.0, 'sell_volume': 500},
# #     'BGRIM': {'total_cost': 426058.53, 'total_volume': 21200, 'avg_cost': 20.0971, 'Market Value': 421879.99999999994, 'sell_volume': 100},
# #     'BEM': {'total_cost': 171840.0, 'total_volume': 22900, 'avg_cost': 7.5039, 'Market Value': 169460.0, 'sell_volume': 0},
# #     'PTTGC': {'total_cost': 255439.41, 'total_volume': 10600, 'avg_cost': 24.0981, 'Market Value': 252280.0, 'sell_volume': 100},
# #     'BJC': {'total_cost': 138780.0, 'total_volume': 5800, 'avg_cost': 23.9276, 'Market Value': 138040.0, 'sell_volume': 0},
# #     'BTS': {'total_cost': 80990.0, 'total_volume': 13400, 'avg_cost': 6.044, 'Market Value': 79730.0, 'sell_volume': 0}
# #     'bTS': {'total_cost': 80990.0, 'total_volume': 13400, 'avg_cost': 6.044, 'Market Value': 79730.0, 'sell_volume': 0}
# #     # The rest of the data can be appended similarly
# # }

# # sum_market = 0
# # for key, value in data.items():
# #     # print(f'{key} : {value['Market Value']}')
# #     if key:
# #         sum_market += value['Market Value']

# # print(sum_market)
# # print(data.get('Market Value'))
# # tmp = sum(list(data.keys()))

# # # Converting the data into a pandas DataFrame
# # df = pd.DataFrame.from_dict(data, orient='index')
# # df = data.sort_values()
# # print(df)
# # print(df['Market Value'])
# # print(df['Market Value'].sum())
# # # print(df.head())

# # df_stock = ['A', 'B']
# # tmp = 'A'    
# # if tmp not in df_stock:
# #     print('tmp')
# from datetime import datetime

# def getday():
#     start_day  = datetime(2024, 12, 23)
#     today  = datetime(2024, 12, 25)
#     # today  = datetime.now()
#     tmp_day = (today - start_day).days
#     day_no = 0
#     if (tmp_day < 7):
#         day_no = tmp_day
#     elif (tmp_day >= 7 and tmp_day <= 11):
#         day_no = tmp_day - 2
#     elif tmp_day >= 14 and tmp_day <= 18:
#         day_no = tmp_day - 4
#     return (day_no)

# # print(getday())
# from datetime import datetime, timedelta

# end_date = datetime(2025, 1, 11)
# delta = timedelta(days=1)
# today = datetime.today()

# def cal_dayNo(today):
#     start_date = datetime(2024, 12, 20)

#     total_days = (today - start_date).days + 1

#     full_weeks, extra_days = divmod(total_days, 7)
#     weekdays = (full_weeks * 5)

#     start_day = start_date.weekday()
#     for i in range(extra_days):
#         if (start_day + i) % 7 < 5:
#             weekdays += 1
#     return weekdays

# print(cal_dayNo(today))
# # while (today < end_date):
# #     print(today)
# #     print(today.strftime("%A"))
# #     print(f"day: {cal_dayNo(today)}")
# #     today += delta

import pandas as pd

# Example balance data (Equity over time)
data = {
    'Equity': [1000000, 1200000, 1150000, 1100000, 1250000, 1050000, 1300000, 1250000, 1000000]
}

df = pd.DataFrame(data)

df['Peak Equity'] = df['Equity'].cummax()
df['Drawdown'] = df['Peak Equity'] - df['Equity']
max_drawdown = df['Drawdown'].max()
min_equity = df['Equity'].min()

# Print results
print(df)
print(f"Maximum Drawdown: {max_drawdown}")
print(f"Minimal Equity: {min_equity}")
