from finta import TA
import pandas as pd
import matplotlib.pyplot as plt


# finTA module web
# https://pypi.org/project/finta/


# Prepare data to use with finta:
#
# finta expects properly formated ohlc DataFrame, with column names in lowercase:
#     ["open", "high", "low", "close"] and ["volume"] for indicators that expect ohlcv input.

# to resample by time period (you can choose different time period)
# ohlc = resample(df, "24h")

# You can also load a ohlc DataFrame from .csv file
# data_file = ("data/bittrex:btc-usdt.csv")
# ohlc = pd.read_csv(data_file, index_col="date", parse_dates=True)


# will return Pandas Series object with the Simple moving average for 42 periods
# TA.SMA(ohlc, 42)

# Load the .csv:
ticker = "BAACEZ"
ohlc = pd.read_csv(f"data/{ticker}.csv", index_col="date", parse_dates=True)

# Now we need to make this ohlc comply to standards.
# We need lowercase column names:
ohlc.columns = ['close', 'volume', 'open', 'high', 'low']


# As you can see some of the values in the DataFrame have a "$" prefix.
# Let's see if we can remove that. You may notice that values have "$" prefix, we must remove that before continuing.
# This small function bellow will do that for us.

# def split(dollar: str) -> float:
#     return float(dollar.split("$")[1])
#
#
# # Now apply it to each column:
# ohlc["close"] = ohlc["close"].apply(split)
# ohlc["low"] = ohlc["low"].apply(split)
# ohlc["high"] = ohlc["high"].apply(split)
# ohlc["open"] = ohlc["open"].apply(split)


# plt.title(f"%K STOCHASTIC OSCILATOR - {ticker}")
# plt.xlabel("date")
# plt.ylabel("%")
# lower line
# plt.plot([2021, 2022], [20, 20], "r-")
# plt.plot([2021, 2022], [80, 80], "r-")
# plt.plot([1,2,3,4,5],[10,20,30,40,50])
# plt.plot(TA.STOCH(ohlc).tail(8), "b-")
# plt.show()


# TA
# Jump right into it to see how easy it is.
low_lewel = 20
mid_level = 50
high_level = 80
stoch_k_result = "-"
stoch_d_result = "-"

print(ticker, "STOCHASTIC")
stoch_k = TA.STOCH(ohlc).tail(2)
for n, row in enumerate(stoch_k):
    if n == 0:
        stoch_k_yesterday_value = row
    elif n == 1:
        stoch_k_today_value = row

stoch_d = TA.STOCHD(ohlc).tail(2)
for n, row in enumerate(stoch_d):
    if n == 0:
        stoch_d_yesterday_value = row
    elif n == 1:
        stoch_d_today_value = row

if stoch_k_today_value > stoch_k_yesterday_value:
    stoch_k_result = "grow up"

print(f"K_yesterday: {stoch_k_yesterday_value}, K_today: {stoch_k_today_value}")
print(stoch_k_result)
print(f"D_yesterday: {stoch_d_yesterday_value}, D_today: {stoch_d_today_value}")
print(stoch_d_result)

print(ticker, "MA")
exit()

print(TA.STOCH(ohlc).tail(8))
print("-" * 40)
print(TA.STOCHD(ohlc).tail(8))
print("end of the line")
exit()

print(TA.RSI(ohlc).tail(4))
# Date
# 2014-12-26    55.099394
# 2014-12-24    43.666451
# 2014-12-23    50.085415
# 2014-12-22    50.594291
# 2014-12-19    38.730709
# 2014-12-18    35.584319
# 2014-12-17    38.632773
# 2014-12-16    32.701255
# 2014-12-15    55.449033
# 2014-12-12    57.338081
# Name: RSI, dtype: float64

# Those are daily candles with standard RSI-14. How about weekly candles and EMA-5?

# Resample the ohlc:
from finta.utils import resample_calendar

# finta.utils has a nice utility: "resample_calendar" which will make nice weekly candles in a jiffy.

weekly_ohlc = resample_calendar(ohlc, "7d")
TA.EMA(weekly_ohlc, 5).tail(10)

# 2019-10-04    1756.299843
# 2019-10-11    1766.693228
# 2019-10-18    1771.388819
# 2019-10-25    1773.145879
# 2019-11-01    1778.163920
# 2019-11-08    1770.309280
# 2019-11-15    1758.442853
# 2019-11-22    1778.465235
# 2019-11-29    1765.803490
# 2019-12-06    1760.108994
# Freq: W-FRI, Name: 5 period EMA, dtype: float64

# That's it, you now know the basics of finta.