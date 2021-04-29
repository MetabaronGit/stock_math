import requests

from bs4 import BeautifulSoup

import csv

import sys


def main():
   '''The main function. Fetches list of locations (as tuples)
   and write results straight to csv.
   '''
   locations = get_locations_list()
   write_to_csv(locations)


def get_locations_list():
   '''Based on user input scrap page and extract location codes with
   their names. Returns list, where locations are represented as tuple
   (code, name).
   '''
   link = input('Insert link with elections results from your desired district: ').strip()
   soup = get_soup(link)

   locations_numbers = get_locations_numbers(soup)
   locations_names = get_locations_names(soup)
   locations_links = get_locations_links(soup)

   return list(zip(locations_numbers, locations_names, locations_links))


def write_to_csv(locations_list):
   '''Expects locations list (as tuple - code, name).
   Ask user for the name of the csv file. Then make header
   for csv file, download election results and in combination with
   location info writes them on the new line in csv file.
   '''
   filename = input('Specify name of your file (without suffix): ').strip()
   link = 'https://www.volby.cz/pls/ps2017nss/' + locations_list[0][2]
   header_soup = get_soup(link)
   header = make_csv_header(header_soup)
   with open('{}.csv'.format(filename), 'w', newline='') as file:
      writer = csv.writer(file)
      writer.writerow(header)
      for location in locations_list:
         print('Currently processing location {}.'.format(location[1]))
         link = 'https://www.volby.cz/pls/ps2017nss/' + location[2]
         soup = get_soup(link)
         results = get_location_results(soup)
         writer.writerow([location[0], location[1]] + results)


def get_soup(link):
   '''Expects link as string.
   Returns BeautifulSoup object to next procession.'''
   try:
      response = requests.get(link)
   except Exception as exc:
      print('There was a problem: %s' % (exc))
      sys.exit()
   return BeautifulSoup(response.text, 'html.parser')


def get_locations_numbers(soup_obj):
   '''Expects soup objects.
   Then fetch td elements with locations numbers.
   In these elements then finds anchor elements and extract their text values
   from then.
   Returns list of locations numbers.'''
   td_elements = get_td_elements(soup_obj, 't1sa1 t1sb1', 't2sa1 t2sb1', 't3sa1 t3sb1')
   td_numbers = []
   for td in td_elements:
      if td.find('a'): # not every td_element must have inner anchor element
         anchor_element = td.find('a')
         td_numbers.append(anchor_element.text) # we need only text of this element
   return td_numbers


def get_locations_names(soup_obj):
   '''Expects soup object.
   Then fetch td elements with locations names and extract locations names
   from then.
   Returns list of locations names.
   '''
   td_elements = get_td_elements(soup_obj, 't1sa1 t1sb2', 't2sa1 t2sb2', 't3sa1 t3sb2')
   return [td.text for td in td_elements]


def get_locations_links(soup_obj):
   '''Expects soup object.
   Then fetch td elements with locations names and extract locations links
   from then.
   Returns list of locations relative links.
   '''
   td_elements = get_td_elements(soup_obj, 't1sa1 t1sb1', 't2sa1 t2sb1', 't3sa1 t3sb1')
   td_links = []
   for td in td_elements:
      if td.find('a'): # not every td_element must have inner anchor element
         anchor_element = td.find('a')
         td_links.append(anchor_element.get('href')) # we need value of href attribute
   return td_links


def get_td_elements(soup_obj, *args):
   '''Expects soup object and arbitrary number of strings,
   representing values of headers attributes.
   Returns list of td elements from the soup.'''
   elements = []
   for arg in args:
      elements += soup_obj.select('td[headers="{}"]'.format(arg))
   return elements


def make_csv_header(soup_obj):
   '''Expects soup object.
   Combines infos and parties names to one header.
   Return list, which will become csv header later.'''
   infos = ['code', 'location', 'registered', 'envelopes', 'valid']
   parties_names = get_parties_names(soup_obj)
   return infos + parties_names


def get_parties_names(soup_obj):
   '''Expects soup object.
   Then fetch td elements with parties names and extract them.
   Returns list of parties names.'''
   elements = get_td_elements(soup_obj, 't1sa1 t1sb2', 't2sa1 t2sb2')
   return [element.text for element in elements if element.text != '-']


def get_location_results(soup_obj):
   '''Expects soup object.
   Returns election results (registered voters, envelopes issued,
   valid votes and parties gains) as list.'''
   return get_info_values(soup_obj) + get_parties_votes(soup_obj)


def get_info_values(soup_obj):
   '''Expects soup object.
   Returns list with registered voters, envelopes issued and valid votes.'''
   info_headers = ['sa2', 'sa3', 'sa6']
   info_values = []
   for info_header in info_headers:
      value_element = soup_obj.find('td', {'headers':'{}'.format(info_header)})
      value_element = value_element.text
      value_element = value_element.replace('\xa0', '') # removing blank space from 2 452 e.g.
      info_values.append(int(value_element))
   return info_values


def get_parties_votes(soup_obj):
   '''Expects soup object.
   Returns list with order parties votes.'''
   elements = get_td_elements(soup_obj, 't1sa2 t1sb3', 't2sa2 t2sb3')
   parties_votes = []
   for element in elements:
      if element.text != '-':
         element = element.text.replace('\xa0', '')
         parties_votes.append(int(element))
   return parties_votes


if __name__ == '__main__':
   main()