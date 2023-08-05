from .models import Anime, Character
from .shortcuts import get

import requests
from bs4 import BeautifulSoup

import time
from concurrent.futures import ThreadPoolExecutor


class Scraper:
    """
    Scrape data from https://myanimelist.net/.
    """

    def __init__(self):
        """
        Initialize the scraper.
        """
        # MAL search url
        self.MAL_ANIME_URL = 'https://myanimelist.net/anime.php?q='
        self.MAL_CHAR_URL = 'https://myanimelist.net/character.php?q='
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
        }

    def search_anime(self, name):
        """
        Args:
            name: Name of anime.

        Returns:
            Return a list of tuple that contains the nane and url of the anime.
        """
        url = self.MAL_ANIME_URL + str(name)
        res = get(url, self.headers)

        if res.status_code != 200:
            raise Exception(f'Response code {res.status_code}.')

        soup = BeautifulSoup(res.text, features='lxml')
        queryset = []

        try:
            div = soup.find(
                'div', {'class': 'js-categories-seasonal js-block-list list'})
            table_rows = div.find_all('tr')[1:6]

            for row in table_rows:
                td = row.find_all('td')[1]
                a = td.find('a')
                queryset.append((a.text, a['href']))
        except Exception as e:
            print(f'Parse Error.\n{e}')

        return queryset

    def get_anime(self, name=None, url=None):
        """
        Get the anime model data. Method only accepts one parameter, either name or url.

        Args:
            name: The name of the anime.
            url: The url of the anime.

        Returns:
            Return the Anime model data.
        """
        anime_url = None

        if name and not url:
            anime_url = self.search_anime(str(name))[0][1]
        elif url and not name:
            anime_url = url
        else:
            raise ValueError('Method needs one parameter, anime or url.')

        return Anime(anime_url)

    def get_all_anime(self, start=0, end=10000):
        """
        Scrape all the anime from the website. Scrapes 50 anime from start to end.
        Note: Stoping the process will result to loss of data.

        Args:
            start: Where to begin scraping.
            end: Where to end scraping.

        Returns:
            Return a list of Anime model data.
        """
        total_anime = end - 50
        count = start
        links = []

        while count <= total_anime:
            url = f'https://myanimelist.net/topanime.php?limit={count}'
            res = get(url, headers=self.headers)
            soup = BeautifulSoup(res.text, features='lxml')

            try:
                aa = soup.find_all(
                    'a', {'class': 'hoverinfo_trigger fl-l fs14 fw-b'})

                for a in aa:
                    link = a['href']

                    if link:
                        links.append(link)
            except Exception as e:
                print(e)

            count += 50

        print(f'Scraping animes total of {len(links)}')

        with ThreadPoolExecutor() as executor:
            animes = executor.map(Anime, links)

        return list(animes)

    def search_character(self, name):
        """
        Args:
            name: Name of the character.

        Returns:
            Return a list of tuple that contains the name and url of the character.
        """
        url = self.MAL_CHAR_URL + str(name)
        res = get(url, headers=self.headers)

        if res.status_code != 200:
            raise Exception(f'Response code {res.status_code}.')

        soup = BeautifulSoup(res.text, features='lxml')
        queryset = []

        try:
            div = soup.find('div', {'id': 'content'})
            table = div.find('table')
            table_rows = table.find_all('tr')[1:6]

            for row in table_rows:
                td = row.find_all('td')[1]
                a = td.find('a')
                queryset.append((a.text, a['href']))
        except Exception as e:
            print(f'Parse Error.\n{e}')

        return queryset

    def get_character(self, name=None, url=None):
        """
        Get the character model data. Method only accepts one parameter, either name or url.

        Args:
            name: Name of the character.
            url: Url of the character.

        Returns:
            Return the Character model data.
        """
        char_url = None

        if name and not url:
            char_url = self.search_character(str(name))[0][1]
        elif url and not name:
            char_url = url
        else:
            raise ValueError('Method needs one parameter, anime or url.')

        return Character(char_url)

    def get_all_characters(self, start=0, end=10000):
        """
        Scrape all the character from the website. Scrapes 50 character from start to end.
        Note: Stoping the process will result to loss of data.

        Args:
            start: Where to begin scraping.
            end: Where to end scraping.

        Returns:
            Return a list of Character model data.
        """
        total_anime = end - 50
        count = start
        links = []

        while count <= total_anime:
            url = f'https://myanimelist.net/character.php?limit={count}'
            res = get(url, headers=self.headers)
            soup = BeautifulSoup(res.text, features='lxml')

            try:
                aa = soup.find('div', {'id': 'content'}).find_all(
                    'a', {'class': 'fs14 fw-b'})

                for a in aa:
                    link = a['href']

                    if link:
                        links.append(link)
            except Exception as e:
                print(e)

            count += 50

        print(f'Scraping animes total of {len(links)}')

        with ThreadPoolExecutor() as executor:
            chars = executor.map(Character, links)

        return list(chars)
