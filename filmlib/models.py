from django.db import models
import datetime


class Movie(models.Model):
    title = models.CharField(db_index=True, max_length=50, blank=False) # Movie name
    poster = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None, blank=True) # Poster from internet...
    about = models.CharField(max_length=500, blank=True) # About Movie
    rait = models.FloatField(blank=True) # movie raiting (family) 
    rait_out = models.FloatField(blank=True) # Raiting (from imdb or others ratings sites)
    director = models.CharField(max_length=50, blank=True) # movie director
    stars = models.CharField(max_length=50, blank=True) # starts of movie ( Keanu Reeves,) 
    genre = models.CharField(max_length=20, blank=True) # movie genre (TODO ad Model Genre)
    add_date = models.DateField(auto_now=False, auto_now_add=False, blank=True)
    release = models.IntegerField(blank=True) # release date


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
        super().save(*args, **kwargs)
