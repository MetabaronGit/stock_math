import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import indicators

# moving average MA
short_period = 50
long_period = 200

# reálná data ze souboru csv
data = pd.read_csv("ČEZ2020_clean.csv")
# print(data.head(period)) #vypsání hlavičky (x řádků souboru csv)

x = data["Datum"].to_numpy()
y = data["Cena_akcie"].to_numpy()

print(f"MA{short_period}: {indicators.MA(short_period, y)}")
print(f"MA{long_period}: {indicators.MA(long_period, y)}")

# zobrazení grafu
# plt.scatter(x[:period], y[:period], c="r")
# otočení popisků datumu o 90 stupňů
# plt.xticks(rotation=90)
# plt.show()


