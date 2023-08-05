import sys

import requests
from bs4 import BeautifulSoup as bs

URL = 'https://pypi.org/search/'
MAX_LEN_DESCRIPTION = 40

def exec_(package_name, with_summary=False):
    global URL
    params = {'q': package_name, 'page': 1}

    answer = 'y'

    result = requests.get(URL, params=params)
    soup = bs(result.content, "html.parser")

    try:
        while answer.lower() == 'y' or answer.lower() == 'yes' or answer == '':
            packages = soup.find('ul', attrs={'aria-label': 'Search results'})
            
            if packages:
                sys.stdout.write("TITLE".ljust(20) + "VERSION".ljust(10) + "DESCRIPTION".ljust(30))
                sys.stdout.write("\n")
                sep = '-' * 50
                sys.stdout.write(sep.ljust(90))
                sys.stdout.write("\n")

            for package in packages.find_all('li'):
                title = package.find('span', attrs={'class': 'package-snippet__name'}).get_text()
                version = package.find('span', attrs={'class': 'package-snippet__version'}).get_text()
                description = ""
                
                if with_summary:
                    description = package.find('p', attrs={'class': 'package-snippet__description'}).get_text()

                sys.stdout.write(title.ljust(20) + version.ljust(10) + description[:MAX_LEN_DESCRIPTION].ljust(30))
                sys.stdout.write("\n")

            sys.stdout.write("\n")
            answer = input('Get results from the next page?: [Yn] ').strip()
            sys.stdout.write("\n\n")
            params['page'] += 1
            result = requests.get(URL, params=params)
            soup = bs(result.content, "html.parser")

    except AttributeError:

        try:
            possible_solution = soup.find('div', attrs={'class': 'callout-block'})
            possible_solution = possible_solution.get_text()\
                                                 .replace('  ', '')\
                                                 .replace('\n', '')
            sys.stdout.write(possible_solution)
        except AttributeError:
            sys.stdout.write("\nNo more results found.\n")

    sys.stdout.write("\n")