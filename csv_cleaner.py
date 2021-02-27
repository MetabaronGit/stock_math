import os
import pandas as pd

# parametry jméno_souboru, jméno_nového_souboru, -r (reverse) otočení od posledního řádku k prvnímu

origin_file = "ČEZ2020_test1.csv"
# origin_file = "ČEZ_prices_test.csv"
new_file = "ČEZ_prices_test_x.csv"

local_path = os.getcwd() + os.sep
# print(local_path)

read_file = open(local_path + origin_file, "r")
new_file = open(local_path + new_file, "w")

new_file_head = read_file.readline()
new_file.write(new_file_head)

lines = reversed(read_file.readlines())

for line in lines:
    line.strip().replace(";", ",")
    new_file.write(line)

read_file.close()
new_file.close()

# print(os.path.isfile(local_path))