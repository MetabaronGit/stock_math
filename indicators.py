def MA(period, data):
    return sum(data[:period]) / len(data[:period])


# swing_low, swing_high, support, resistance, uptrend, downtrend
# uptrend -> začne klesat, max - low = firstSupport, max - mid = secondSupport (při otočení zpět do uptrendu signal Buy)
# exit strategy -> stoploss cca 55 %
# target profit ->
def fibonaci(min: float, max: float) -> list:
    price_range = max - min
    mid = min + price_range / 2
    low = min + price_range / 100 * 38.2
    top = min + price_range / 100 * 61.8

    # print("-" * 21)
    # print(f"fibonacci retracement")
    # print("-" * 21)
    # print(f"(max) {max}")
    # print(f" (61) {top}")
    # print(f" (50) {mid}")
    # print(f" (38) {low}")
    # print(f"(min) {min}")

    return [low, mid, top]


def RSI_14(value_yesterday: float, value_today: float) -> str:
    """
    perioda 14, 30/70
    """
    result = "neutral"
    if value_yesterday <= 50 and value_today > 50:
        result = "BUY signal "
    elif value_yesterday >= 50 and value_today < 50:
        result = "SELL signal "
    elif value_today > 70:
        result = "trend will turn down "
    elif value_today < 30:
        result = "trend will turn up "
    return result

# všechny hodnoty z PSE

# 16.3.21, BAACEZ, close=537,
# RSI_14=68.86 %,

# 17.3.21, BAACEZ, close=541, min=538, max=544, obj_tis=129,04, RMS, min=535, max=545, close=543
# RSI_14=71.38 %
# BB, top=550, mid=532, low=514


print(f"fib:", fibonaci(535, 545))
# close price
# stock name


print(f"RSI:", RSI_14(68.86, 71.38))
