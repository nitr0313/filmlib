from django.shortcuts import render
from bs4 import BeautifulSoup
import requests 


base_search_url = 'https://www.kinopoisk.ru/index.php?kp_query={}'
base_url = 'https://www.kinopoisk.ru{}'
big_img_url = 'https://www.kinopoisk.ru/images/film_big/{}'


def home(request):
    return render(request, 'filmlib/index.html')


def add_movie(request):
    return render(request, 'filmlib/add_movie.html')


def movie_search(request):
    url = base_search_url.format(request.POST.get('movie_name'), False)

    res = requests.get(url)
    data = res.text
    soup = BeautifulSoup(data, features='html.parser')
    movies_list = soup.find_all('div', {'class': 'element'})
    res = []
    index = 0
    for movie in movies_list:
        raw_name = movie.find(class_='name')
        name = raw_name.text
        if 'data-type="person"' in name or 'data-type="place"' in name:
            continue
        main_url = raw_name.find("a").get("data-url")
        data_id = raw_name.find("a").get("data-id")

        raw_rate = movie.find(class_='rating')
        if raw_rate:
            rate = raw_rate.text
        else:
            rate = '0'

        res.append((name,rate,base_url.format(main_url),big_img_url.format('.'.join([data_id,'jpg']))))
        index += 1

    con = {
        'movies': res,
        'url': url,
        'search_results': True
    }
    return render(request, 'filmlib/add_movie.html', context = con)
