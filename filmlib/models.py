from django.db import models
import datetime
from .utils import gen_slug
from django.conf import settings


class Movie(models.Model):
    title = models.CharField(db_index=True, max_length=50, blank=False) # Movie name
    poster = models.URLField(max_length=200,default='', null=True) # Poster from internet...
    about = models.CharField(max_length=500, default='', blank=True, null=True) # About Movie
    rait = models.FloatField(blank=True, default=0.0, null=True) # movie raiting (family)
    rait_home = models.FloatField(blank=True, default=0.0, null=True) # Raiting (from imdb or others ratings sites)
    director = models.CharField(max_length=50, default='', blank=True, null=True) # movie director
    stars = models.CharField(max_length=250, default='', blank=True, null=True) # starts of movie ( Keanu Reeves,)
    genre = models.CharField(max_length=100, default='', blank=True, null=True) # movie genre (TODO ad Model Genre)
    add_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    release = models.IntegerField(blank=True, default=1900, null=True) # release date
    duration = models.CharField(max_length=10, default='00:00:00', null=True) # duration time
    kinopoisk_id = models.IntegerField(db_index=True, blank=True, default=0) # 
    slug = models.SlugField(default='')

    # def get_create_url(self, kino_id):
    #     return reverse('add_new_movie', {*args, **kwargs})

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"

    def __str__(self):
        return f"{self.title} ({self.release})"

    def save(self, *args, **kwargs):
        if not self.id:
            self.add_date = datetime.datetime.now()
            self.rait_home = 0.0
            self.slug = gen_slug(self.kinopois_id, True)
        super().save(*args, **kwargs)
