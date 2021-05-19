import os
import csv


def main():
    # změní formát data v csv souboru na yyyy-mm-dd a vytvoří nový soubor typu .bak
    header = ["date", "close", "volume", "open", "high", "low"]
    ticker = "BAACEZ"
    if os.path.isfile(f"data/{ticker}.csv"):
        final_csv = list()
        with open(f"data/{ticker}.csv", "r") as f:
            f_reader = csv.reader(f)
            for row in f_reader:
                new_date_format = row[0][6:] + "-" + row[0][3:5] + "-" + row[0][:2]
                row[0] = new_date_format
                final_csv.append(row)
            final_csv.pop(0)

        with open(f"data/{ticker}.bak", "w", newline="") as f:
            f_writer = csv.writer(f)
            f_writer.writerow(header)
            f_writer.writerows(final_csv)

    else:
        print(f"file data/{ticker}.csv not found")


if __name__ == "__main__":
    main()
