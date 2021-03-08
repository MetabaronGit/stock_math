def MA(period, data):
    return sum(data[:period]) / len(data[:period])

