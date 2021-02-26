import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# moving average MA

# reálná data ze souboru csv
data = pd.read_csv("ČEZ_prices_test.csv")
print(data.head()) #vypsání hlavičky (prvních pět řádků souboru csv)

# numpy pole od 0 do 833 ve dne 14.6.2019
x = np.arange(len(data))
# Ceny převedeme na numpy pole
y = data["Cena_akcie"].to_numpy()


# zobrazení grafu
plt.scatter(x, y, c="r")
plt.show()
