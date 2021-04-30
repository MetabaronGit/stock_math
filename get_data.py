import requests
from bs4 import BeautifulSoup as BS
import datetime
import sys

URL = "https://www.penize.cz/burza-cennych-papiru-praha/"

WEB_TABLE_HEADER = ['Datum',
                    'Změna',
                    'Objem v ks',
                    'Objem v tis. Kč',
                    'Otevírací kurz v Kč',
                    'Min. kurz v Kč',
                    'Max. kurz v Kč',
                    'Zavírací kurz v Kč']

TICKER = dict(BAAAVAST="334228-avast",
              BAACEZ="6143-cez",
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
        print("table header check: OK")
    else:
        print("table header check: ERROR!")
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


def save_data_to_csv():
    pass


def get_data_from_csv():
    pass


def main():
    try:
        # ticker = sys.argv[1]
        ticker = "BAACEZ"
        url = URL + TICKER[ticker]
        print(url)
        soup = get_soup(url)
    except Exception:
        print("Špatně zadaný ticker.")
        # ToDo: logování chyb
        exit()

    data_table = get_data(soup)

    today = datetime.datetime.now()
    # today_date = today.strftime("%d.%m.%Y")

    x = today - datetime.timedelta(days=1)
    yesterday_date = x.strftime("%d.%m.%Y")

    print("yesterday date:", yesterday_date)
    print("data:", data_table.get(yesterday_date))


if __name__ == "__main__":
    main()