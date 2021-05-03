import requests
from bs4 import BeautifulSoup as BS
import datetime
import csv
import time
import sys

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

TICKER = dict(BAAAVAST="334228-avast",
              BAACEZ=dict(ticker="6143-cez", quoteitemid="6143", marketid="44427"),
              BAACZGCE="334231-czg",
              BAAERBAG="6122-erste-bank",
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


def save_data_to_csv(file_name: str, header: list, data: list) -> None:
    """Zapíše získané údaje do souboru csv"""
    try:
        with open(file_name, "w", newline="", encoding='utf-8') as f:
            f_writer = csv.writer(f)
            f_writer.writerow(header)
            f_writer.writerows(data)
        LOG_BOOK.append(f"Soubor {file_name} byl vytvořen.")
    except Exception as e:
        LOG_BOOK.append(f"Chyba při vytváření souboru {file_name}.")
        print_log()
        exit()


def get_data_from_csv():
    pass

def create_url(ticker: str, month: int, year: int) -> str:
    """Sestaví url dle zadaných parametrů."""
    url = URL + URL_PARAMS.format(ticker=TICKER[ticker]["ticker"],
                                  quoteitemid=TICKER[ticker]["quoteitemid"],
                                  marketid=TICKER[ticker]["marketid"],
                                  month=month,
                                  year=year)
    return url

def main():
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
        url = create_url(ticker, actual_month, actual_year)
        LOG_BOOK.append(f"actual_month url: {url}")
        soup = get_soup(url)
        LOG_BOOK.append(f"get_soup from actual_month url: OK")
        actual_month_data_table = get_data(soup)
        LOG_BOOK.append("actual_month_data_table: OK")

        if len(actual_month_data_table) < 14:
            url = create_url(ticker, previous_month, previous_year)
            LOG_BOOK.append(f"previous_month url: {url}")
            time.sleep(2)
            soup = get_soup(url)
            LOG_BOOK.append(f"get_soup from actual_month url: OK")
            previous_month_data_table = get_data(soup)
            LOG_BOOK.append("previous_month_data_table: OK")
            print("počet zápisů:", len(previous_month_data_table))

    except Exception as e:
        LOG_BOOK.append(f"chyba: {e}")
        print_log()
        exit()

    print("yesterday date:", yesterday_date)
    print("data:", actual_month_data_table.get(yesterday_date))
    print(previous_month_data_table.get("30.04.2021"))

    print_log()


if __name__ == "__main__":
    main()
