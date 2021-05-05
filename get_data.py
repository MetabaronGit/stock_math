import requests
from bs4 import BeautifulSoup as BS
import datetime
import csv
import time
import os

URL = "https://www.penize.cz/burza-cennych-papiru-praha/"
URL_PARAMS = "{ticker}?quoteitemid={quoteitemid}&marketid={marketid}&month={month}&year={year}#historyTable"

WEB_TABLE_HEADER = ['Datum',
                    'Změna',
                    'Objem v ks',
                    'Objem v tis. Kč',
                    'Otevírací kurz v Kč',
                    'Min. kurz v Kč',
                    'Max. kurz v Kč',
                    'Zavírací kurz v Kč']
# https://www.penize.cz/burza-cennych-papiru-praha/334228-avast?quoteitemid=334228&marketid=44427&month=5&year=2021#historyTable
TICKER = dict(BAAAVAST="334228-avast",
              BAACEZ=dict(ticker="6143-cez", quoteitemid="6143", marketid="44427"),
# https://www.penize.cz/burza-cennych-papiru-praha/334231-czg?quoteitemid=334231&marketid=44427&month=5&year=2021#historyTable
              BAACZGCE="334231-czg",
# https://www.penize.cz/burza-cennych-papiru-praha/6122-erste-bank?quoteitemid=6122&marketid=44427&month=5&year=2021#historyTable
              BAAERBAG="6122-erste-bank",
# https://www.penize.cz/burza-cennych-papiru-praha/326262-moneta-money-bank?quoteitemid=326262&marketid=44427&month=5&year=2021#historyTable
              BAAGECBA="326262-moneta-money-bank",
              BAAKOMB="6103-komercni-banka",
              BAASTOCK="334227-stock",
              BAATABAK="6150-philip-morris-cr",
              BAATELEC="6141-o2-c-r",
              BAAVIG="42198-vig",
              BABKOFOL="326261-kofola-cs",
              BAAPEN="334226-photon-energy")

LOG_BOOK = []


def get_soup(url: str) -> BS:
    content = requests.get(url)
    soup = BS(content.text, "html.parser")
    return soup


def get_data(soup: BS) -> dict:
    table = soup.find("div", class_="sortingTable", style="overflow-x: auto;")

    lines = table.find_all("tr")

    actual_web_table_header = []
    for name in lines[0]:
        actual_web_table_header.append(name.text)

    if check_table_header(actual_web_table_header):
        LOG_BOOK.append("table header check: OK")
    else:
        LOG_BOOK.append("table header check: ERROR!")
        print_log()
        exit()

    result = dict()
    for line in lines:
        values = line.find_all("td")

        column = 0
        for value in values:
            if column == 0:
                date = str(value.text)
            elif column == 2:
                volume = int(value.text.replace("\xa0", ""))
            elif column == 4:
                open = float(value.text.replace(",", "."))
            elif column == 5:
                low = float(value.text.replace(",", "."))
            elif column == 6:
                high = float(value.text.replace(",", "."))
            elif column == 7:
                close = float(value.text.replace(",", "."))

            column += 1
            if column > 7:
                column = 0
                result[date] = {"volume": volume, "open": open, "low": low, "high": high, "close": close}
    return result


def check_table_header(header: list) -> bool:
    """
    Ověří seřazení sloupců a jejich počet. Pokud je vše OK vrací True.

    :param header: aktuální list názvů sloupců získaný z webu
    :return: bool
    """
    return header == WEB_TABLE_HEADER


def print_log():
    print(LOG_BOOK)

    with open("logs/log.txt", "a", encoding='utf-8') as f:
        for line in LOG_BOOK:
            f.write(line + "\n")
        f.write("-" * 20 + "\n")


def save_data_to_csv(file_name: str, data: list) -> None:
    """Zapíše získané údaje do souboru csv.
    """
    header = ["date", "close", "volume", "open", "high", "low"]
    try:
        with open(file_name, "w", newline="", encoding='utf-8') as f:
            f_writer = csv.writer(f)
            f_writer.writerow(header)
            f_writer.writerows(data)
        LOG_BOOK.append(f"Soubor {file_name} byl vytvořen.")
    except Exception as e:
        LOG_BOOK.append(f"Chyba při vytváření souboru {file_name}.")


def get_data_from_csv(file: str) -> dict:
    """Zapíše získané údaje ze souboru csv do slovníku.
       hlavička csv je: date,close,volume,open,high,low
    """
    result = dict()
    with open(file, "r") as f:
        f_reader = csv.reader(f)
        next(f_reader)
        for line in f_reader:
            result[line[0]] = {"close": line[1], "volume": line[2], "open": line[3], "high": line[4], "low": line[5]}
    return result


def create_url(ticker: str, month: int, year: int) -> str:
    """Sestaví url dle zadaných parametrů."""
    url = URL + URL_PARAMS.format(ticker=TICKER[ticker]["ticker"],
                                  quoteitemid=TICKER[ticker]["quoteitemid"],
                                  marketid=TICKER[ticker]["marketid"],
                                  month=month,
                                  year=year)
    return url


def main():
    actual_month_data_table = dict()
    previous_month_data_table = dict()
    csv_data_table = dict()
    final_data_table = dict()

    today = datetime.datetime.now()
    today_date = today.strftime("%d.%m.%Y")
    yesterday_date = (today - datetime.timedelta(days=1)).strftime("%d.%m.%Y")
    actual_month = int(today.strftime("%m"))
    actual_year = int(today.strftime("%Y"))
    previous_month = int((today - datetime.timedelta(days=30)).strftime("%m"))
    previous_year = int((today - datetime.timedelta(days=30)).strftime("%Y"))
    # print(previous_month, previous_year)
    # print(actual_month, actual_year)

    LOG_BOOK.append(f"spuštění dne: {today_date}")
    try:
        # ticker = sys.argv[1]
        ticker = "BAACEZ"
        LOG_BOOK.append(f"ticker: {ticker}")

        """
        # načtení dat z csv souboru
        if os.path.isfile(f"data/{ticker}.csv"):
            LOG_BOOK.append(f"file data/{ticker}.csv exists: check")
            csv_data_table = get_data_from_csv(f"data/{ticker}.csv")
            LOG_BOOK.append(f"get data from csv file: check")
        else:
            LOG_BOOK.append(f"file data/{ticker}.csv doesn't exists.")
        """

        # načtení dat z webu (aktuální měsíc)
        url = create_url(ticker, actual_month, actual_year)
        LOG_BOOK.append(f"actual_month url: {url}")
        soup = get_soup(url)
        LOG_BOOK.append(f"get_soup from actual_month url: OK")
        actual_month_data_table = get_data(soup)
        LOG_BOOK.append("actual_month_data_table: OK")

        # if len(actual_month_data_table) < 14:
        # načtení dat z webu (předchozí měsíc)
        url = create_url(ticker, previous_month, previous_year)
        LOG_BOOK.append(f"previous_month url: {url}")
        time.sleep(2)
        soup = get_soup(url)
        LOG_BOOK.append(f"get_soup from actual_month url: OK")
        previous_month_data_table = get_data(soup)
        LOG_BOOK.append("previous_month_data_table: OK")
        # print("počet zápisů:", len(previous_month_data_table))

        # sestavení finální datové struktury (list) od nejstaršího data (opačně než na webu)
        # header = ["date", "close", "volume", "open", "high", "low"]
        # previous_month_data_table.update(actual_month_data_table)
        final_data_table = dict(sorted(previous_month_data_table.items()))
        previous_month_data_table = dict(sorted(previous_month_data_table.items()))
        actual_month_data_table = dict(sorted(actual_month_data_table.items()))

        final_list = []
        for key in previous_month_data_table:
            line_list = []
            line_list.append(str(key))
            line_list.append(previous_month_data_table[key]["close"])
            line_list.append(previous_month_data_table[key]["volume"])
            line_list.append(previous_month_data_table[key]["open"])
            line_list.append(previous_month_data_table[key]["high"])
            line_list.append(previous_month_data_table[key]["low"])
            final_list.append(line_list)

        for key in actual_month_data_table:
            line_list = []
            line_list.append(str(key))
            line_list.append(actual_month_data_table[key]["close"])
            line_list.append(actual_month_data_table[key]["volume"])
            line_list.append(actual_month_data_table[key]["open"])
            line_list.append(actual_month_data_table[key]["high"])
            line_list.append(actual_month_data_table[key]["low"])
            final_list.append(line_list)

        # uložení dat do csv souboru
        save_data_to_csv(f"data/{ticker}.csv", final_list)
        LOG_BOOK.append(f"csv file saved: check")

    except Exception as e:
        LOG_BOOK.append(f"chyba: {e}")
        print_log()
        exit()

    # print("data:", actual_month_data_table.get(yesterday_date))
    # print(previous_month_data_table.get("30.04.2021"))

    print_log()


if __name__ == "__main__":
    main()
