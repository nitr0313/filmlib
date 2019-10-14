
from bs4 import BeautifulSoup
import requests
# import requests_cache
from django.shortcuts import render


# requests_cache.install_cache('cache_')

# base_url = 'https://www.kinopoisk.ru/film/{}/'
base_url = 'https://www.kinopoisk.ru/level/1/film/{}/sr/1/'
big_img_url = 'https://www.kinopoisk.ru/images/film_big/{}'

def soup_cooking(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 YaBrowser/19.9.3.314 Yowser/2.5 Safari/537.36'
      }
    resp = requests.get(url, headers = headers)
    data = resp.text
    if 'checkcaptcha' in data:
        print('Доступ временно заблокирован капчой')
        return 'captcha', data
    soup = BeautifulSoup(data, features='html.parser')
    return soup



def get_movie_info(kino_id):
    print(f'utils->get_movie_info->kino_id = {kino_id}')
    url = base_url.format(kino_id)
    soup = soup_cooking(url)
    if soup[0] == 'captcha':
        return {
            'title': 'kinopoisk.ru заблокировал меня',
            soup[0]: soup[1]
        }
    res = soup.findAll('meta', {'itemprop':'description'})
    about = ''
    if res:
        about = '\n'.join([ x.get('content') for x in res])

    duration = soup.find('meta', {'itemprop':'duration'}).get('content', '')
    title = soup.find('meta', {'itemprop':'name'}).get('content', '')
    poster = big_img_url.format('.'.join((kino_id,'jpg')))
    rait = soup.find('span', {'class':'rating_ball'}).text
    director = soup.find('td', {'itemprop':'director'}).text
    stars = ''
    genre = soup.find('span', {'itemprop':'genre'}).text
    release = ''
    reult = {
        'title':title,
        'duration':duration,
        'poster':poster,
        'rait':rait,
        'director':str(director),
        'genre':genre,
        'stars':stars,
        'release':release
        }
    return reult