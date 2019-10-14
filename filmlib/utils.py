
from bs4 import BeautifulSoup
import requests
# import requests_cachecls

# base_url = 'https://www.kinopoisk.ru/film/{}/'
base_url = 'https://www.kinopoisk.ru/level/1/film/{}/sr/1/'
big_img_url = 'https://www.kinopoisk.ru/images/film_big/{}'

def soup_cooking(url):
    resp = requests.get(url)
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
        return {'title': 'kinopoisk.ru заблокировал меня'}
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
        'director':director,
        'genre':genre,
        'stars':stars,
        'release':release
        }
    return reult