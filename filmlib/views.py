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
    req = request.POST.get('movie_name', False)
    result = []
    url = ''
    if req:
        print(req)
        url = base_search_url.format(req)
        print(url)

        res = requests.get(url)
        data = res.text
        soup = BeautifulSoup(data, features='html.parser')
        movies_list = soup.find_all('div', {'class': 'element'})
        print(movies_list)
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

            result.append((name,rate,main_url,big_img))
            index += 1

    con = {
        'movies': result,
        'url': url,
        'search_results': True
    }
    return render(request, 'filmlib/add_movie.html', context = con)
