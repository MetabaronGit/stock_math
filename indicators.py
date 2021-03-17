def MA(period, data):
    return sum(data[:period]) / len(data[:period])

def fibonaci(min, max):
    price_range = max - min
    mid = min + price_range / 2
    low = min + price_range / 100 * 38.2
    top = min + price_range / 100 * 61.8

    print("-" * 21)
    print(f"fibonacci retracement")
    print("-" * 21)
    print(f"(max) {max}")
    print(f" (61) {top}")
    print(f" (50) {mid}")
    print(f" (38) {low}")
    print(f"(min) {min}")

    return [low, mid, top]


print(fibonaci(535, 545))
# close price
# stock name