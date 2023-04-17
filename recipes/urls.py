from django.urls import path

from recipes.views import sobre, home


urlpatterns = [
    path('', home),   # Home
    path('sobre/', sobre)    # sobre
]
