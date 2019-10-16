
from bs4 import BeautifulSoup
import requests
import requests_cache
from django.shortcuts import render
from django.utils.text import slugify
from time import time



requests_cache.install_cache('cache_')

# base_url = 'https://www.kinopoisk.ru/film/{}/'
base_url = 'https://www.kinopoisk.ru/level/1/film/{}/sr/1/'
big_img_url = 'https://www.kinopoisk.ru/images/film_big/{}'

dic_data = {
    'title': 'Кавказская пленница, или Новые приключения Шурика',
    'duration': '01:19:53',
    'poster': 'https://www.kinopoisk.ru/images/film_big/44745.jpg',
    'rait': '8.458',
    'director': ' Леонид Гайдай',
    'genre': ' комедия,  приключения,  мелодрама,  семейный,  музыка',
    'stars': 'Александр Демьяненко, Наталья Варлей, Юрий Никулин, Георгий Вицин, Евгений Моргунов',
    'release': '1966',
    'about':'''Отправившись в одну из горных республик собирать фольклор, герой фильма Шурик влюбляется в симпатичную девушку — «спортсменку, отличницу, и просто красавицу». Но ее неожиданно похищают, чтобы насильно выдать замуж. Наивный Шурик не сразу смог сообразить, что творится у него под носом, — однако затем отважно ринулся освобождать «кавказскую пленницу»…''',
    'kinopoisk_id' : '44745'

    }


def gen_slug(s, uniquie=True):
    new_slug = slugify(s, allow_unicode=True)
    if uniquie:
        return new_slug + '-' + str(int(time()))
    else:
        return new_slug


def soup_cooking(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 YaBrowser/19.9.3.314 Yowser/2.5 Safari/537.36'
      }
    resp = requests.get(url, headers = headers)
    data = resp.text
    if 'checkcaptcha' in data:
        print('Доступ временно заблокирован капчой')
        return False
    soup = BeautifulSoup(data, features='html.parser')
    return soup



def get_movie_info(kino_id):
    print(f'utils->get_movie_info->kino_id = {kino_id}')
    url = base_url.format(kino_id)
    soup = soup_cooking(url)
    if not soup:
        return False, dic_data
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
    result = {
        'title':title,
        'duration':duration,
        'poster':poster,
        'rait':rait,
        'director':str(director),
        'genre':genre,
        'stars':stars,
        'release':release,
        'kinopoisk_id':kino_id,
        'about':' '
        }
    return True, result