from bs4 import BeautifulSoup
from requests import HTTPError

from .shortcuts import get


class Anime:
    def __init__(self, url):
        print(f'Scraping {url}')

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
        }
        res = get(url, headers=headers)
        self._soup = BeautifulSoup(res.text, features='lxml')
        self.url = url

    @property
    def title(self):
        title = None

        try:
            div = self._soup.find('div', {'id': 'contentWrapper'})
            span = div.find('span', {'itemprop': 'name'})
            title = span.text
        except:
            print('Anime: Skipping title.')

        return title

    @property
    def english_title(self):
        title = None

        try:
            divs = self._soup.find_all('div', {'class': 'spaceit_pad'})

            for div in divs:
                if 'English:' in div.text:
                    title = div.text.replace('English:', '').rstrip().lstrip()
                    break
        except:
            print('Anime: Skipping english title.')

        return title

    @property
    def japanese_title(self):
        title = None

        try:
            divs = self._soup.find_all('div', {'class': 'spaceit_pad'})

            for div in divs:
                if 'Japanese:' in div.text:
                    title = div.text.replace('Japanese:', '').rstrip().lstrip()
                    break
        except:
            print('Anime: Skipping japanese title .')

        return title

    @property
    def synonyms(self):
        syn = None

        try:
            divs = self._soup.find_all('div', {'class': 'spaceit_pad'})

            for div in divs:
                if 'Synonyms:' in div.text:
                    syn = div.text.replace(
                        'Synonyms:', '').rstrip().lstrip()
                    break
        except:
            print('Anime: Skipping synonyms.')

        return syn

    @property
    def synopsis(self):
        synopsis = ''

        try:
            span = self._soup.find('span', {'itemprop': 'description'})
            synopsis = span.text
        except:
            print('Anime: Skipping synopsis.')

        return synopsis

    @property
    def animetype(self):
        atype = None

        try:
            divs = self._soup.find(
                'div', {'class': 'js-scrollfix-bottom'}).find_all('div')

            for div in divs:
                if 'Type:' in div.text:
                    atype = div.text.replace('Type:', '').rstrip().lstrip()
                    break
        except:
            print('Anime: Skipping anime type.')

        return atype

    @property
    def episodes(self):
        eps = None

        try:
            divs = self._soup.find(
                'div', {'class': 'js-scrollfix-bottom'}).find_all('div',
                                                                  {'class': 'spaceit'})

            for div in divs:
                if 'Episodes:' in div.text:
                    eps = div.text.replace('Episodes:', '').rstrip().lstrip()
                    break
        except:
            print('Anime: Skipping episodes.')

        return eps

    @property
    def genres(self):
        genres = None

        try:
            divs = self._soup.find(
                'div', {'class': 'js-scrollfix-bottom'}).find_all('div')

            for div in divs:
                if 'Genres:' in div.text:
                    genres = div.text.replace('Genres:', '').rstrip().lstrip()
                    break
        except:
            print('Anime: Skipping genres.')

        return genres

    @property
    def poster(self):
        poster = None

        try:
            img = self._soup.find('img', {'class': 'ac'})
            poster = img['src']
        except:
            print('Anime: Skipping poster.')

        return poster

    @property
    def trailer(self):
        trailer = None

        try:
            a = self._soup.find(
                'a', {'class': 'iframe js-fancybox-video video-unit promotion'})
            trailer = a['href']
        except:
            print('Anime: Skipping trailer.')

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
        return f'<models.Anime {id(self)}>'


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
        name = None

        try:
            div = self._soup.find('div', {'id': 'content'}).find('table').find(
                'td', {'style': 'padding-left: 5px;', 'valign': 'top'}).find(
                'div', {'class': 'normal_header'})
            name = div.text
        except:
            print('Character: Skipping name.')

        return name

    @property
    def alternate_names(self):
        name = None

        try:
            div = self._soup.find('div', {'id': 'contentWrapper'}).find('div')
            h1 = div.find('h1', {'class': 'h1'})
            name = h1.text.split('"', 2)[1]
        except:
            print('Character: Skipping alternate names.')

        return name

    @property
    def poster(self):
        poster = None

        try:
            img = self._soup.find('div', {'id': 'content'}).find('img')
            poster = img['src']
        except:
            print('Character: Skipping poster.')

        return poster

    def get_gallery(self):
        url = self._url + '/pictures'
        res = get(url, headers=self.headers)
        soup = BeautifulSoup(res.text, features='lxml')
        gallery = []

        try:
            imgs = soup.find('div', {'id': 'content'}).find(
                'td', {'style': 'padding-left: 5px;', 'valign': 'top'}).find(
                'table').find_all('img')

            for i, img in enumerate(imgs):
                try:
                    gallery.append(img['src'])
                except:
                    print(f'Character: Skipping gallery image #{i + 1}.')
        except:
            print('Character: Skipping Gallery.')

        return gallery

    def __repr__(self):
        return f'<models.Character {id(self)}>'
