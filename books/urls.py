from django.conf import settings
from django.conf.urls import url
from django.views.static import serve

from books.views import *
from django.conf.urls.static import static
from django.urls import path
from django.contrib import admin
urlpatterns = [


    path('',index, name='start'),
    # path('allbooks/', listbooks),
    path('stat_czyt/', stat_czyt, name='czytelnik'),
    path('stat_msc/', stat_msc, name='miesiac'),
    path('stat_klasa/', stat_klasa, name='klasa'),
    path('stat_klasa_sem/', stat_klasa_sem, name='klasa_sem'),
    # path('rejestracja/', register, name='rejestracja'),
    # path('logowanie/', login, name='logowanie'),
    # path('logowanie/', login, name='logowanie'),
    path('admin/', admin1, name='admin1'),



    ]
admin.site.site_header = 'Biblioteka'
