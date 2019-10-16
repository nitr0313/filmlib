from django import forms
from .models import Movie


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            'title','poster','about',
            'rait','rait_home','director',
            'stars','genre','add_date',
            'release','duration','kinopois_id',
        ]
