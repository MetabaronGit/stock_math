import os

# parametry jméno_souboru, jméno_nového_souboru, -r (reverse) otočení od posledního řádku k prvnímu

FILE_TYPE = ".csv"
local_path = os.getcwd() + os.sep

origin_file = "ČEZ2020_test1"
new_file = origin_file + "_ok"

read_file = open(local_path + origin_file + FILE_TYPE, "r")
new_file = open(local_path + new_file + FILE_TYPE, "w")

new_file_head = read_file.readline().replace(";", ",")
new_file.write(new_file_head)

lines = reversed(read_file.readlines())

for line in lines:
    line = line.replace(";", ",")
    new_file.write(line)

read_file.close()
new_file.close()

print("csv file clearing complete")
# print(os.path.isfile(local_path))