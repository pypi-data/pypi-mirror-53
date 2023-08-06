from .models import Anime, Character
from .shortcuts import get

from bs4 import BeautifulSoup

from concurrent.futures import ThreadPoolExecutor


class Scraper:
    """
    Scrape data from https://myanimelist.net/.
    """

    def __init__(self, request_interval=2, max_request=999):
        """
        Initialize scraper.
        """
        # MAL URLS
        self.BASE_URL = 'https://myanimelist.net'
        self.ANIME_SEARCH_URL = self.BASE_URL + '/anime.php?q='
        self.CHARACTER_SEARCH_URL = self.BASE_URL + '/character.php?q='
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) '
                          'Gecko/20100101 Firefox/68.0'
        }
        self.request_interval = request_interval
        self.max_request = max_request

    def search_anime(self, name):
        """
        Search the anime.

        Args:
            name: Name of anime.

        Returns:
            Return a list of tuple that contains the nane and url of the anime.

        Raises:
            TypeError: Argument 'name' must be string.
        """
        if type(name) != str:
            raise TypeError("Argument 'name' must be string.")

        url = self.ANIME_SEARCH_URL + name
        res = get(url, headers=self.headers,
                  interval=self.request_interval, max=self.max_request)
        soup = BeautifulSoup(res.text, features='lxml')
        queryset = []

        try:
            div = soup.find('div', {'id': 'content'}).find(
                'div', {'class': 'js-categories-seasonal js-block-list list'})
            table_rows = div.find('table').find_all('tr')[1:6]

            for row in table_rows:
                td = row.find_all('td')[1]
                a = td.find('a')
                queryset.append((a.text, a['href']))
        except Exception as e:
            print(f'Error at search_anime.\n{e}')

        return queryset

    def get_anime(self, name):
        """
        Get the anime model data.

        Args:
            name: The name of the anime.

        Returns:
            Return the Anime model data.

        Raises:
            TypeError: Argument 'name' must be string.
        """
        if type(name) != str:
            raise TypeError("Argument 'name' must be string.")

        url = self.search_anime(str(name))[0][1]
        return Anime(url)

    def get_all_anime(self, start=0, end=10000):
        """
        Scrape all the anime from the website. Scrapes 50 anime from start to
        end.
        Note: Stopping the process will result to loss of data.

        Args:
            start: Where to begin scraping.
            end: Where to end scraping.

        Returns:
            Return a list of Anime model data.
        """
        up_to = end - 50
        count = start
        links = []

        print(f'Parsing total of {end - start}')

        while count <= up_to:
            url = self.BASE_URL + '/topanime.php?limit=' + str(count)
            res = get(url, headers=self.headers,
                      interval=self.request_interval, max=self.max_request)

            # Parse the response data.
            soup = BeautifulSoup(res.text, features='lxml')

            try:
                div = soup.find('div', {'id': 'content'}).find(
                    'div', {'class': 'pb12'})
                rows = div.find(
                    'table', {'class': 'top-ranking-table'}).find_all('tr', {'class': 'ranking-list'})

                for i, row in enumerate(rows):
                    a = row.find('div', {'class': 'detail'}).find(
                        'a', {'class': 'hoverinfo_trigger fl-l fs14 fw-b'})
                    links.append(a['href'])
            except Exception as e:
                print(f'Error at get_all_anime.\n{e}')

            count += 50

        print(f'Scraping total of {len(links)} anime.')

        animes = [Anime(url) for url in links]
        return animes

    def get_character(self, name):
        """
        Get character data.

        Args:
            name: Name of the character.

        Returns:
            Return the Character model data.

        Raises:
            TypeError: Argument 'name' must be string.
        """
        if type(name) != str:
            raise TypeError("Argument 'name' must be string.")

        url = self.search_character(name)[0][1]
        return Character(url)

    def search_character(self, name):
        """
        Search the character. Note that searches are not 100% accurate. To compensate,
        this returns 5 search results. Each result is a tuple containing the name then then url of the character.

        Args:
            name: Name of the character.

        Returns:
            Return a list of tuple containing name and url of the character.

        Raises:
            TypeError: Argument 'name' must be string.
        """
        if type(name) != str:
            raise TypeError("Argument 'name' must be string.")

        url = self.CHARACTER_SEARCH_URL + name
        res = get(url, headers=self.headers,
                  interval=self.request_interval, max=self.max_request)
        soup = BeautifulSoup(res.text, features='lxml')
        queryset = []

        try:
            # {'width': '100%', 'cellspacing': '0', 'cellpadding': '0', 'border': '0'}
            table = soup.find('div', {'id': 'content'}).find_next(
                'table')
            table_rows = table.find_all('tr')

            for row in table_rows[1:6]:
                a = row.find(
                    'td', {'class': 'borderClass bgColor1', 'width': '175'}).find('a')
                queryset.append((a.text, a['href']))
        except Exception as e:
            print(f'Error at search_character.\n{e}')

        return queryset

    def get_all_characters(self, start=0, end=10000):
        """
        Scrape all the anime from the website. Scrapes 50 anime from start to
        end.
        Note: Stopping the process will result to loss of data.

        Args:
            start: Where to begin scraping.
            end: Where to end scraping.

        Returns:
            Return a list of Anime model data.
        """
        up_to = end - 50
        count = start
        links = []

        print(f'Parsing total of {end - start}')

        while count <= up_to:
            url = self.BASE_URL + '/character.php?limit=' + str(count)
            res = get(url, headers=self.headers,
                      interval=self.request_interval, max=self.max_request)

            # Parse the response data.
            soup = BeautifulSoup(res.text, features='lxml')

            try:
                table = soup.find('div', {'id': 'content'}).find(
                    'table', {'class': 'characters-favorites-ranking-table'})
                table_rows = table.find_all('tr', {'class': 'ranking-list'})

                for row in table_rows:
                    a = row.find('td', {'class': 'people'}).find(
                        'div', {'class': 'information di-ib mt24'}).find('a')
                    links.append(a['href'])
            except Exception as e:
                print(f'Error at get_all_characters.\n{e}')

            count += 50

        print(f'Scraping total of {len(links)} anime.')

        characters = [Character(url) for url in links]
        return characters
