import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import indicators

# moving average MA
period = 5

# reálná data ze souboru csv
data = pd.read_csv("ČEZ_prices_test.csv")
print(data.head(period)) #vypsání hlavičky (x řádků souboru csv)

# numpy pole od 0
# x = np.arange(len(data))
x = data["Datum"].to_numpy()
# Ceny převedeme na numpy pole
y = data["Cena_akcie"].to_numpy()

print(f"MA: {indicators.MA(period, y)}")

# zobrazení grafu
plt.scatter(x[:period], y[:period], c="r")
# otočení popisků datumu o 90 stupňů
plt.xticks(rotation=90)
plt.show()




# import argparse
# # create parser
# descStr = "This program converts an image into ASCII art."
# parser = argparse.ArgumentParser(description=descStr)
# # add expected arguments
# parser.add_argument('--file', dest='imgFile', required=True)
# parser.add_argument('--scale', dest='scale', required=False)
# parser.add_argument('--out', dest='outFile', required=False)
# parser.add_argument('--cols', dest='cols', required=False)
# parser.add_argument('--morelevels', dest='moreLevels', action='store_true')
#
# # parse args
# args = parser.parse_args()
#
# imgFile = args.imgFile