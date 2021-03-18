import datetime


def day_name_cz(day_name_en: str) -> str:
    """
    Přeloží název dne z angličtiny do češtiny.

    :param day_name_en: jméno dne v angličtině
    :return: jméno dne v češtině
    """
    days = {"sunday": "neděle",
            "monday": "pondělí",
            "tuesday": "úterý",
            "wednesday": "středa",
            "thursday": "čtvrtek",
            "friday": "pátek",
            "saturday": "sobota"}
    if day_name_en.lower() in days:
        return days[day_name_en.lower()]
    else:
        return day_name_en


def MA(period, data):
    return sum(data[:period]) / len(data[:period])


# swing_low, swing_high, support, resistance, uptrend, downtrend
# uptrend -> začne klesat, max - low = firstSupport, max - mid = secondSupport (při otočení zpět do uptrendu signal Buy)
# exit strategy -> stoploss cca 55 %
# target profit ->

# všechny hodnoty brány z PSE

def read_values(ticker: str, *values) -> list:
    """
    Načtení hodnot z obchodování ze souboru CSV

    :param ticker: Kód akcie
    :param values: hodnoty z obchodování po zavření trhu
    :return: list s hodnotami za daný den a den předtím
    """
    # ToDo: podle data načtení dnešních a včerejších hodnot ze souboru csv
    # ToDo: pokud datum nenajde, hláška, že data nejsou
    # ToDo: najde soubor podle tickeru
    today = datetime.datetime.now()
    today_date = today.strftime("%d.%m.%Y")

    with open(f"{ticker}_data.csv", "r") as file:
        previous_line = ""
        for line in file:
            if line[:10] == today_date:
                result = line.split(",") + previous_line.split(",")
            else:
                result = []
            previous_line = line
    return result

def fibonaci(min: float, max: float) -> list:
    """
    SMA period 20
    """
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
    Relative Strength Index, period 14, 30/70
    """
    HIGH_LEVEL = 70
    LOW_LEVEL = 30
    result = "neutral"
    if value_yesterday <= 50 and value_today > 50:
        result = "BUY signal "
    elif value_yesterday >= 50 and value_today < 50:
        result = "SELL signal "
    elif value_today > HIGH_LEVEL and value_yesterday < value_today:
        result = "neutral - trend will turn down "
    elif value_today > HIGH_LEVEL and value_yesterday >= value_today:
        result = "SELL signal - trend will turn down "
    elif value_today < LOW_LEVEL and value_yesterday > value_today:
        result = "neutral - trend will turn up "
    elif value_today < LOW_LEVEL and value_yesterday <= value_today:
        result = "BUY signal - trend will turn up "
    return result


def prediction():
    x = datetime.datetime.now()
    today_date = x.strftime("%d.%m.%Y")  # anglický název dne
    print("-" * 50)
    print(f"Dnešní datum: {today_date}, {day_name_cz(x.strftime('%A'))}".center(50))
    print("-" * 50)

    print(read_values("BAACEZ"))

    print(f"RSI:", RSI_14(71.38, 70.99))
    # print(f"fib:", fibonaci(535, 545))


prediction()
