from django.db.models import Sum, Count
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings


from . models import *
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Extract
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from . forms import SignUpForm
import calendar


# Create your views here.
# @login_required(login_url='login-page')
# def listbooks(request):
#     booksall = Books.objects.all()
#     return render (request, 'books/booksall.html', {'booksall':booksall})


def index(request):
    set = settings.BASE_DIR
    set1 = settings.MEDIA_URL
    static = settings.STATIC_URL
    static_root = settings.STATIC_ROOT

    return render (request, 'books/index.html', {'set1':set1, 'static':static, 'static_root':static_root})


@login_required(login_url='admin1')
def stat_czyt(request):
    ilosc_wyp = len(Wypozyczenia.objects.all())
    ilosc_wyp_czytelnik = Wypozyczenia.objects.values('czytelnik').annotate(ilosc=Count('czytelnik')).values('czytelnik__family','czytelnik__name','czytelnik__klasa_id__name','czytelnik_id','ilosc').order_by('czytelnik__klasa_id__name','-ilosc')

    il = 0

    return render (request, 'books/stat_czyt.html', {'ilosc_wyp_czytelnik':ilosc_wyp_czytelnik})

@login_required(login_url='admin1')
def stat_msc(request):

    il = 0
    ilosc_wyp_month = Wypozyczenia.objects.values(month=Extract('take_date', 'month')).annotate(ilosc=Count(Extract('take_date', 'month'))).values('ilosc', 'month', 'czytelnik_id')
    return render (request, 'books/stat_msc.html', {'ilosc_wyp_month':ilosc_wyp_month, })

@login_required(login_url='admin1')
def stat_klasa(request):

    ilosc_wyp_klasa_sem_1 = Wypozyczenia.objects.values('czytelnik__klasa_id__name').annotate(
        ilosc=Count('czytelnik__klasa_id__name'), month=Extract('take_date', 'month')).values(
        'czytelnik__klasa_id__name', 'ilosc', 'month').order_by('month').filter(month__lte='12' ) &\
                            Wypozyczenia.objects.values('czytelnik__klasa_id__name').annotate(
        ilosc=Count('czytelnik__klasa_id__name'), month=Extract('take_date', 'month')).values(
        'czytelnik__klasa_id__name', 'ilosc', 'month').order_by('month').filter(month__gte='9') | Wypozyczenia.objects.values('czytelnik__klasa_id__name').annotate(
        ilosc=Count('czytelnik__klasa_id__name'), month=Extract('take_date', 'month')).values(
        'czytelnik__klasa_id__name', 'ilosc', 'month').order_by('month').filter(month='1' )

    ilosc_wyp_klasa_sem_2 = Wypozyczenia.objects.values('czytelnik__klasa_id__name').annotate(
        ilosc=Count('czytelnik__klasa_id__name'), month=Extract('take_date', 'month')).values(
        'czytelnik__klasa_id__name', 'ilosc', 'month').order_by('month').filter(month__lte='6') & \
                            Wypozyczenia.objects.values('czytelnik__klasa_id__name').annotate(
                                ilosc=Count('czytelnik__klasa_id__name'), month=Extract('take_date', 'month')).values(
                                'czytelnik__klasa_id__name', 'ilosc', 'month').order_by('month').filter(
                                month__gte='2')

    ile2 = len(ilosc_wyp_klasa_sem_2)


    return render(request, 'books/stat_klasa.html', {'ilosc_wyp_klasa_sem_1': ilosc_wyp_klasa_sem_1, 'ilosc_wyp_klasa_sem_2': ilosc_wyp_klasa_sem_2,'ile2':ile2})



@login_required(login_url='admin1')
def stat_klasa_sem(request):

    ilosc_wyp_klasa_sem_1 = (Wypozyczenia.objects.values('czytelnik__klasa_id__name').annotate(ilosc=Count('czytelnik__klasa_id__name')
       ).\
        values('czytelnik__klasa_id__name','ilosc', month=Extract('take_date', 'month')).filter(month__lte='12' ) & Wypozyczenia.objects.values('czytelnik__klasa_id__name').annotate(ilosc=Count('czytelnik__klasa_id__name')

                                                                      ). \
        values('czytelnik__klasa_id__name', 'ilosc', month=Extract('take_date', 'month')).filter(month__gte='9') | Wypozyczenia.objects.values('czytelnik__klasa_id__name').annotate(ilosc=Count('czytelnik__klasa_id__name')
                                                                      ). \
        values('czytelnik__klasa_id__name', 'ilosc', month=Extract('take_date', 'month')).filter(month='1')).values('czytelnik__klasa_id__name').annotate(ilosc=Count('czytelnik__klasa_id'))

    ilosc_wyp_klasa_sem_2 = (Wypozyczenia.objects.values('czytelnik__klasa_id__name').annotate(
        ilosc=Count('czytelnik__klasa_id__name')
        ). \
                             values('czytelnik__klasa_id__name', 'ilosc', month=Extract('take_date', 'month')).filter(
        month__lte='6') & Wypozyczenia.objects.values('czytelnik__klasa_id__name').annotate(
        ilosc=Count('czytelnik__klasa_id__name')

        ).values('czytelnik__klasa_id__name', 'ilosc', month=Extract('take_date', 'month')).filter(
        month__gte='2')) .values('czytelnik__klasa_id__name').annotate(ilosc=Count('czytelnik__klasa_id'))
    ile_sem2 = len(ilosc_wyp_klasa_sem_2)

    return render(request, 'books/stat_klasa_sem.html', {'ilosc_wyp_klasa_sem_1': ilosc_wyp_klasa_sem_1,'ilosc_wyp_klasa_sem_2': ilosc_wyp_klasa_sem_2,'ile_sem2':ile_sem2})




@csrf_exempt
def register(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # messages.success(request, "Rejestracja zakończona")
            return  HttpResponse("Rejestracja zakończona")

    return render(request,'books/register.html', {'form':form})

@csrf_exempt
def login(request):
    # status = False
        if request.user.is_authenticated:
            return redirect('wypozyczone')



        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(username=username, password=password)
                print('login haslo ',user)
                return redirect('start')
        form = AuthenticationForm()


        return render(request, 'books/login.html', {'form':form})


def admin1(request):
    response = redirect('/admin/')
    return response



