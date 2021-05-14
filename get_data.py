import requests
from bs4 import BeautifulSoup as BS
import datetime
import csv
import time
import os
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

TICKER = dict(BAAAVAST=dict(ticker="334228-avast", quoteitemid="334228", marketid="44427"),
              BAACEZ=dict(ticker="6143-cez", quoteitemid="6143", marketid="44427"),
              BAACZGCE=dict(ticker="334231-czg", quoteitemid="334231", marketid="44427"),
              BAAERBAG=dict(ticker="6122-erste-bank", quoteitemid="6122", marketid="44427"),
              BAAGECBA=dict(ticker="326262-moneta-money-bank", quoteitemid="326262", marketid="44427"),
              BAAKOMB=dict(ticker="6103-komercni-banka", quoteitemid="6103", marketid="44427"),
              BAASTOCK=dict(ticker="334227-stock", quoteitemid="334227", marketid="44427"),
              BAATABAK=dict(ticker="6150-philip-morris-cr", quoteitemid="6150", marketid="44427"),
              BAATELEC=dict(ticker="6141-o2-c-r", quoteitemid="6141", marketid="44427"),
              BAAVIG=dict(ticker="42198-vig", quoteitemid="42198", marketid="44427"),
              BABKOFOL=dict(ticker="326261-kofola-cs", quoteitemid="326261", marketid="44427"),
              BAAPEN=dict(ticker="334226-photon-energy", quoteitemid="334226", marketid="44427"))

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
        f.write("-" * 80 + "\n")


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


def save_current_day_data_to_csv(file: str, data: list) -> None:
    """Zapíše získané údaje do souboru csv.
    """
    header = ["ticker", "close", "volume", "open", "high", "low", "barometer"]
    try:
        if os.path.exists(file):
            os.remove(file)
        with open(file, "w", newline="", encoding='utf-8') as f:
            f_writer = csv.writer(f)
            f_writer.writerow(header)
            f_writer.writerows(data)
        LOG_BOOK.append(f"Soubor {file} byl vytvořen.")
    except Exception as e:
        LOG_BOOK.append(f"Chyba při vytváření souboru {file}.")


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


def get_last_day_data(soup: BS) -> dict:
    result = dict()
    ticker = dict(ČEZ="BAACEZ")
    table = soup.find("tbody")
    lines = table.find_all("tr")
    for line in lines:
        values = line.find_all("td")
        column = 0
        for value in values:
            if column == 0:
                ticker = value.find("a").text
            if column == 1:
                barometer = int(value.find("span").text.replace("-", "0"))
            if column == 2:
                close = value.text.replace("\xa0", "").replace(",", ".").replace("Kč", "").replace("-", "0")
            if column == 4:
                open = value.text.replace("\xa0", "").replace(",", ".").replace("Kč", "").replace("-", "0")
            if column == 5:
                low_high_list = value.text.replace("\xa0", "").replace(",", ".").replace("-", "0").split("Kč")
                low = float(low_high_list[0])
                if len(low_high_list) > 1:
                    high = float(low_high_list[1])
                else:
                    high = 0.0
            if column == 6:
                volume_list = value.text.replace("\xa0", "").replace(" ", "").replace("-", "0").split("ks")
                volume = int(volume_list[0])

            column += 1
            if column > 7:
                column = 0
                result[ticker] = {"volume": volume, "open": open, "low": low,
                                  "high": high, "close": close, "barometer": barometer}
    return result


def get_current_day_data() -> list:
    pse_tickers = dict(BAACEZ="ČEZ", BAACZGCE="CZG", BAAERBAG="ERSTE GROUP BANK",
                       BABKOFOL="KOFOLA ČS", BAAKOMB="KOMERČNÍ BANKA", BAAGECBA="MONETA MONEY BANK",
                       BAATELEC="O2 C.R.", BAAVIG="VIG", BAATABAK="PHILIP MORRIS ČR", BAAPEN="PHOTON ENERGY",
                       BAAAVAST="AVAST", BAASTOCK="STOCK")

    url_list = ["https://www.pse.cz/udaje-o-trhu/akcie/prime-market",
                "https://www.pse.cz/udaje-o-trhu/akcie/standard-market",
                "https://www.pse.cz/udaje-o-trhu/akcie/free-market"]

    final_list = []
    for url in url_list:
        soup = get_soup(url)
        LOG_BOOK.append(f"get_soup from url {url}: OK")
        time.sleep(2)
        last_day_data = get_last_day_data(soup)

        for key in last_day_data:
            if key in pse_tickers.values():
                line_list = []
                # najití klíče podle hodnoty ve slovníku
                line_list.append(list(pse_tickers.keys())[list(pse_tickers.values()).index(key)])
                # line_list.append(str(key))
                line_list.append(last_day_data[key]["close"])
                line_list.append(last_day_data[key]["volume"])
                line_list.append(last_day_data[key]["open"])
                line_list.append(last_day_data[key]["high"])
                line_list.append(last_day_data[key]["low"])
                line_list.append(last_day_data[key]["barometer"])
                final_list.append(line_list)

    return final_list


def main():
    actual_month_data_table = dict()
    previous_month_data_table = dict()
    csv_data_table = dict()
    final_data_table = dict()

    today = datetime.datetime.now()
    today_date = today.strftime("%d.%m.%Y")
    current_time = today.strftime("%H:%M:%S")
    yesterday_date = (today - datetime.timedelta(days=1)).strftime("%d.%m.%Y")
    actual_month = int(today.strftime("%m"))
    actual_year = int(today.strftime("%Y"))
    previous_month = int((today - datetime.timedelta(days=30)).strftime("%m"))
    previous_year = int((today - datetime.timedelta(days=30)).strftime("%Y"))
    # print(previous_month, previous_year)
    # print(actual_month, actual_year)

    LOG_BOOK.append(f"spuštění dne: {today_date}, v čase: {current_time}")
    try:
        # ToDo: parametry pro shell
        # -all DATE -> uloží kompletní historii od data DATE do nového souboru, pokud soubor existuje
        # přidá do jména (x) číslo kopie

        # -last -> do souboru csv přidá na konec záznam z posledního obch. dne (kontrola data, jestli tam už není)
        # pokud soubor neexistuje, spustí nejprve verzi -2m

        # -actualize -> projde csv soubor a dopln9 chzbějící dny

        # -2m -> vytvoří csv z posledních 2 měsíců od aktuálního data


        # parameter = sys.argv[1].lower()
        # ticker = sys.argv[2].upper()
        ticker = "BAAAVAST"
        parameter = "-all"
        date_from = "01.01.2020"
        LOG_BOOK.append(f"parameter: {parameter}, ticker: {ticker}")

        """
        # načtení dat z csv souboru
        if os.path.isfile(f"data/{ticker}.csv"):
            LOG_BOOK.append(f"file data/{ticker}.csv exists: check")
            csv_data_table = get_data_from_csv(f"data/{ticker}.csv")
            LOG_BOOK.append(f"get data from csv file: check")
        else:
            LOG_BOOK.append(f"file data/{ticker}.csv doesn't exists.")
        """

        if parameter == "-l":
            # ToDo: kontrola data vytvoření / datum poslední změny
            # (last) stáhne data pouze z aktuálního dne, až po uzavření burzy
            # vytvoří temp file s daty z aktuálního dne
            temp_file = "data/temp.csv"

            if current_time > "18:00":
                LOG_BOOK.append("starting time: OK")

                if os.path.isfile(temp_file):
                    # kontrola data souboru temp_file
                    t = datetime.datetime.fromtimestamp(os.path.getctime(temp_file))
                    temp_file_creation_date = t.strftime("%d.%m.%Y")
                    if temp_file_creation_date == today_date:
                        print("temp file is actual:", temp_file_creation_date)
                        LOG_BOOK.append(f"temp file is actual: {temp_file_creation_date}")
                    else:
                        print("temp file is out of date")
                        LOG_BOOK.append(f"temp file is out of date: {temp_file_creation_date}")
                        final_list = get_current_day_data()
                        save_current_day_data_to_csv(temp_file, final_list)
                else:
                    print("creating temp file...")
                    final_list = get_current_day_data()
                    save_current_day_data_to_csv(temp_file, final_list)

            else:
                LOG_BOOK.append("bad starting time (current_time < 18:00), temp file not created")

        elif parameter == "-2m":
            # (2 months) načtení dat z webu (aktuální měsíc + předchozí)
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

# https://www.penize.cz/burza-cennych-papiru-praha/334228-avast?quoteitemid=334228&marketid=44427&month=5&year=2021#historyTable
# https://www.penize.cz/burza-cennych-papiru-praha/334231-czg?quoteitemid=334231&marketid=44427&month=5&year=2021#historyTable
# https://www.penize.cz/burza-cennych-papiru-praha/6122-erste-bank?quoteitemid=6122&marketid=44427&month=5&year=2021#historyTable
