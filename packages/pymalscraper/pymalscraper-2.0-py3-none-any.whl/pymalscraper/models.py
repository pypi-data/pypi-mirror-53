import time
import requests
from bs4 import BeautifulSoup

from .shortcuts import get


class Anime:
    def __init__(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
        }
        res = get(url, headers=headers)
        self._soup = BeautifulSoup(res.text, features='lxml')
        print(f'Scraped {url}')

    @property
    def title(self):
        title = ''

        try:
            span = self._soup.find('span', {'itemprop': 'name'})
            title = span.text
        except Exception as e:
            print(f'Error getting title.\nError: {e}')

        return title

    @property
    def english_title(self):
        title = ''

        try:
            divs = self._soup.find_all('div', {'class': 'spaceit_pad'})

            for div in divs:
                if 'English:' in div.text:
                    title = div.text.replace('English:', '').rstrip().lstrip()
                    break
        except Exception as e:
            print(f'Error getting english title.\nError: {e}')

        return title

    @property
    def japanese_title(self):
        title = ''

        try:
            divs = self._soup.find_all('div', {'class': 'spaceit_pad'})

            for div in divs:
                if 'Japanese:' in div.text:
                    title = div.text.replace('Japanese:', '').rstrip().lstrip()
                    break
        except Exception as e:
            print(f'Error getting japanese title.\nError: {e}')

        return title

    @property
    def synonyms(self):
        syn = ''

        try:
            divs = self._soup.find_all('div', {'class': 'spaceit_pad'})

            for div in divs:
                if 'Synonyms:' in div.text:
                    syn = div.text.replace(
                        'Synonyms:', '').rstrip().lstrip()
                    break
        except Exception as e:
            print(f'Error getting synonyms.\nError: {e}')

        return syn

    @property
    def synopsis(self):
        synopsis = ''

        try:
            span = self._soup.find('span', {'itemprop': 'description'})
            synopsis = span.text
        except Exception as e:
            print(f'Error getting synopsis.\nError: {e}')

        return synopsis

    @property
    def animetype(self):
        atype = ''

        try:
            divs = self._soup.find(
                'div', {'class': 'js-scrollfix-bottom'}).find_all('div')

            for div in divs:
                if 'Type:' in div.text:
                    atype = div.text.replace('Type:', '').rstrip().lstrip()
                    break
        except Exception as e:
            print(f'Error getting type.\nError: {e}')

        return atype

    @property
    def episodes(self):
        eps = ''

        try:
            divs = self._soup.find(
                'div', {'class': 'js-scrollfix-bottom'}).find_all('div', {'class': 'spaceit'})

            for div in divs:
                if 'Episodes:' in div.text:
                    eps = div.text.replace('Episodes:', '').rstrip().lstrip()
                    break
        except Exception as e:
            print(f'Error getting episodes.\nError: {e}')

        return eps

    @property
    def genres(self):
        genres = ''

        try:
            divs = self._soup.find(
                'div', {'class': 'js-scrollfix-bottom'}).find_all('div')

            for div in divs:
                if 'Genres:' in div.text:
                    genres = div.text.replace('Genres:', '').rstrip().lstrip()
                    break
        except Exception as e:
            print(f'Error getting genres.\nError: {e}')

        return genres

    @property
    def poster(self):
        poster = ''

        try:
            img = self._soup.find('img', {'class': 'ac'})
            poster = img['src']
        except Exception as e:
            print(f'Error getting poster.\nError: {e}')

        return poster

    @property
    def trailer(self):
        trailer = ''

        try:
            a = self._soup.find(
                'a', {'class': 'iframe js-fancybox-video video-unit promotion'})
            trailer = a['href']
        except Exception as e:
            print(f'Error getting trailer.\nError: {e}')

        return trailer

    def get_data(self):
        """
        Gets the full anime data in json.

        Returns:
            Dict object.
        """
        data = {
            'title': self.title,
            'english_title': self.english_title,
            'japanese_title': self.japanese_title,
            'synonyms': self.synonyms,
            'synopsis': self.synopsis,
            'type': self.animetype,
            'episodes': self.episodes,
            'genres': self.genres,
            'poster': self.poster,
            'trailer': self.trailer
        }

        return data

    def __repr__(self):
        return f'<models.Anime \'{self.title}\'>'


class Character:
    def __init__(self, url):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
        }
        res = get(url, headers=self.headers)
        self._soup = BeautifulSoup(res.text, features='lxml')
        self._url = url
        print(f'Scraped {url}')

    @property
    def name(self):
        name = ''

        try:
            div = self._soup.find('div', {'id': 'content'}).find(
                'td', {'style': 'padding-left: 5px;', 'valign': 'top'}).find('div', {'class': 'normal_header'})
            name = div.text
        except Exception as e:
            print(f'Error at name.\nError: {e}')

        return name

    @property
    def poster(self):
        poster = ''

        try:
            img = self._soup.find('div', {'id': 'content'}).find('img')
            poster = img['src']
        except Exception as e:
            print(f'Error at posters.\nError: {e}')

        return poster

    def get_gallery(self):
        url = self._url + '/pictures'
        res = get(url, headers=self.headers)
        soup = BeautifulSoup(res.text, features='lxml')
        imgs = soup.find('div', {'id': 'content'}).find(
            'td', {'style': 'padding-left: 5px;', 'valign': 'top'}).find('table').find_all('img')
        gallery = []

        for img in imgs:
            if img['src']:
                gallery.append(img['src'])

        return gallery

    def __repr__(self):
        return f'<models.Character \'{self.name}\'>'
