
from bs4 import BeautifulSoup
import requests

base_url = 'https://www.kinopoisk.ru{}'

def get_movie_info(kino_id):
    print(f'utils->get_movie_info->kino_id = {kino_id}')
    return {'title':'test'}