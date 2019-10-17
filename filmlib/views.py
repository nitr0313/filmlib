from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
import requests
from .utils import get_movie_info
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
from .forms import MovieForm
from .models import Movie

DEBUG = settings.DEBUG

base_search_url = 'https://www.kinopoisk.ru/index.php?kp_query={}'
base_url = 'https://www.kinopoisk.ru{}'
big_img_url = 'https://www.kinopoisk.ru/images/film_big/{}'


def home(request):
    mv = Movie.objects.all()
    con = {
        'movies':mv
    }
    return render(request, 'filmlib/index.html', context = con)


class AddMovie(View):
    def get(self, request, id):
        ans, dic_data = get_movie_info(id)
        if not ans:
            # return render(request, 'filmlib/kinopoisk_captcha.html', context=dic_data)
            # return HttpResponse(dic_data['captcha'])
            print('Нас щаблочили!')

        ls = ['title','rait','director','stars','about','poster',
            'rait_out',
            'genre','add_date','release', 'kinopoisk_id']
        result = []
        for field in ls:
            result.append(dic_data.get(field, ''))

        con = dic_data

        # con = {
        #     'movie': result,
        # }
        return render(request, 'filmlib/add_movie.html', context=con)

    def post(self, request, id):
        # If all OK, redirect to deteail movie
        print(request.POST)
        movie_form = MovieForm(request.POST)
        if movie_form.is_valid():
            print('С формой все ок!')
            new_movie = movie_form.save()
            return redirect('home')
        else:
            print('Что-то не так с формой!')
        return render(request, 'filmlib/add_movie.html', context={'movie': movie_form.data, '':movie_form.errors})     
        



# def add_movie(request):
#     return render(request, 'filmlib/search_movie.html')


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
            kinopoisk_id = raw_name.find("a").get("data-id") # id in kinopoisk datebase
            mv = Movie.objects.all().filter(kinopoisk_id=kinopoisk_id)
            raw_url = raw_name.find("a").get("data-url")

            name = raw_name.text # Movie name
            main_url = base_url.format(raw_url) # Url of main page movie kinopoisk.ru

            raw_rate = movie.find(class_='rating') # Movie Rating
            big_img = big_img_url.format('.'.join([kinopoisk_id,'jpg'])) # Poster image

            if raw_rate:
                rate = raw_rate.text
            else:
                rate = '0'

            result.append((name,rate,main_url,big_img,kinopoisk_id))
            index += 1

    con = {
        'movies': result,
        'url': url,
        'search_results': True
    }
    return render(request, 'filmlib/search_movie.html', context = con)
