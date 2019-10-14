from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from .utils import get_movie_info
from django.views.generic import View
from django.http import HttpResponse

DEBAG = True

base_search_url = 'https://www.kinopoisk.ru/index.php?kp_query={}'
base_url = 'https://www.kinopoisk.ru{}'
big_img_url = 'https://www.kinopoisk.ru/images/film_big/{}'


def home(request):
    return render(request, 'filmlib/index.html')


class AddMovie(View):
    def get(self, request, id):
        if DEBAG:
            dic_data = {
                'title': 'Кавказская пленница, или Новые приключения Шурика',
                'duration': '01:19:53',
                'poster': 'https://www.kinopoisk.ru/images/film_big/44745.jpg',
                'rait': '8.458',
                'director': ' Леонид Гайдай',
                'genre': ' комедия,  приключения,  мелодрама,  семейный,  музыка',
                'stars': '',
                'release': '1964',
                'about':'''Отправившись в одну из горных республик собирать фольклор, герой фильма Шурик влюбляется в симпатичную девушку — «спортсменку, отличницу, и просто красавицу». Но ее неожиданно похищают, чтобы насильно выдать замуж.

                        Наивный Шурик не сразу смог сообразить, что творится у него под носом, — однако затем отважно ринулся освобождать «кавказскую пленницу»…'''
                }
        else:
            dic_data = get_movie_info(id)
        if 'captcha' in dic_data:
            # return render(request, 'filmlib/kinopoisk_captcha.html', context=dic_data)
            return HttpResponse(dic_data['captcha'])

        ls = ['title','rait','director','stars','about','poster',
            'rait_out',
            'genre','add_date','release']
        result = []
        for field in ls:
            result.append(dic_data.get(field, ''))

        con = {
            'movie': result,
        }
        return render(request, 'filmlib/add_movie.html', context=con)

    def post(self, request):
        # If all OK, redirect to deteail movie
        pass



def add_movie(request):
    return render(request, 'filmlib/search_movie.html')


def movie_search(request):
    # TODO <a href="/lists/navigator/sci-fi/?quick_filters=films">фантастика</a>
    req = request.POST.get('movie_name', False)
    result = []
    url = ''
    if req:
        url = base_search_url.format(req)

        res = requests.get(url)
        data = res.text
        soup = BeautifulSoup(data, features='html.parser')
        movies_list = soup.find_all('div', {'class': 'element'})
        index = 0
        for movie in movies_list:
            raw_name = movie.find(class_='name')
            if 'data-type="person"' in raw_name or 'data-type="place"' in raw_name:
                continue
            raw_url = raw_name.find("a").get("data-url")

            name = raw_name.text # Movie name
            main_url = base_url.format(raw_url) # Url of main page movie kinopoisk.ru
            data_id = raw_name.find("a").get("data-id") # id in kinopoisk datebase
            raw_rate = movie.find(class_='rating') # Movie Rating
            big_img = big_img_url.format('.'.join([data_id,'jpg'])) # Poster image

            if raw_rate:
                rate = raw_rate.text
            else:
                rate = '0'

            result.append((name,rate,main_url,big_img,data_id))
            index += 1

    con = {
        'movies': result,
        'url': url,
        'search_results': True
    }
    return render(request, 'filmlib/search_movie.html', context = con)
