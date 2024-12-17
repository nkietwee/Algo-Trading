
import pandas as pd
import os

# # file_path = os.path.expanduser("/home/nkietwee/Desktop/competition_api/Result/summary/*.csv")
# # file_path = os.path.expanduser("/home/nkietwee/Desktop/competition_api/Result/summary/024_LuckNa_summary.csv")
# file_path = os.path.expanduser("/home/nkietwee/Desktop/Daily_Ticks.csv")

file_path = os.path.expanduser('/home/nkietwee/Desktop/competition_api/Result/portfolio/024_LuckNa_portfolio.csv') 
df = pd.read_csv(file_path)
df = df
print(df)
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