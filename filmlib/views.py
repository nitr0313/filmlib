from django.shortcuts import render
from bs4 import BeautifulSoup
import requests 


def home(request):
    return render(request, 'filmlib/index.html')


def add_movie(request):
    return render(request, 'filmlib/add_movie.html')


def movie_search(request):
    base_url = 'https://www.kinopoisk.ru/index.php?kp_query={}'

    url = base_url.format(request.POST.get('movie_name'), False)

    res = requests.get(url)
    data = res.text
    soup = BeautifulSoup(data, features='html.parser')
    movies_list = soup.find_all('a', {'class': 'js-serp-metrika'})
    print(movies_list[0:5])
    con = {
        'url': url
    }
    return render(request, 'filmlib/add_movie.html', context = con)


