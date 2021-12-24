from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from datetime import date
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError
from django.contrib import messages

class Klasa(models.Model):
    name = models.CharField(max_length=255, default='', verbose_name='Klasa', unique=True)

    def save(self):
        self.name = self.name.upper()
        super(Klasa, self).save()



    class Meta:
         verbose_name = "Klasa"
         verbose_name_plural = "Klasa"


    def __str__(self):
        return self.name


class Users_take(models.Model):
    name = models.CharField(max_length=255, default='', verbose_name='Imię')
    family = models.CharField(max_length=255, default='', verbose_name='Nazwisko')
    klasa_id = models.ForeignKey(Klasa, on_delete=models.CASCADE, verbose_name='Klasa')


    class Meta:
         verbose_name = "Czytelnik"
         verbose_name_plural = "Czytelnik"


    def __str__(self):
        return self.name + ' ' + self.family

    def delete(self):
        users = Users_take.objects.get(name__in=['-----'])
        if not users:
            for user in users:
                user.delete()
        super(Users_take, self).delete()




class Kategoria(models.Model):
    title_kat = models.CharField(max_length=255, default='',unique=True,verbose_name='Nazwa')
    class Meta:
           verbose_name_plural = "Kategoria"
    def __str__(self):
        return self.title_kat






class Books(models.Model):
    title = models.CharField(max_length=255, default='', verbose_name='Tytuł')
    description = models.TextField(default='brak', verbose_name='Opis')
    number =  models.IntegerField(verbose_name='Nr książki', unique=True)
    # number =  models.IntegerField(editable=False)
    publicated_year = models.IntegerField(default=2000, verbose_name='Data publikacji')
    author_family =  models.CharField(max_length=255, default='', verbose_name='Nazwisko autora')
    author_name = models.CharField(max_length=255, default='', verbose_name='Imię autora')
    image = models.ImageField(upload_to='books/media', default='sdc19018.jpg', blank=True)
    # available = models.BooleanField(default=True, verbose_name='Dostępność')
    available = models.BooleanField(editable=True, verbose_name='Dostępność', default=True)
    kategoria_id = models.ForeignKey(Kategoria, blank=True, on_delete=models.SET_NULL, null=True, verbose_name='Kategoria')

    def family_color(self):
        if self.available:
              return '<div style="width:100%%; height:100%%; background-color:orange;">%s</div>' % self.author_family
        return mark_safe('<div style="width:100%%; height:100%%; background-color:orange;">%s</div>' % self.author_family)

    def image_tag(self):
        return mark_safe('<img src="books/media/%s" width="50" height="50" />' % (self.image))

    image_tag.short_description = 'Image'

    class Meta:
        verbose_name_plural = "Książka"
        verbose_name = "Książka"

    def __str__(self):
        return self.title +' nr '+ str( self.number)

    # def save(self, *args, **kwargs):
    #     if len(Books.objects.all()) == 0:
    #         print('ilosc book', len(Books.objects.all()))
    #         self.number = 1
    #         super(Books, self).save()
    #     self.number=  Books.objects.last().number +1
    #     print('ilosc book', len(Books.objects.all()))
    #     super(Books, self).save(*args, **kwargs)






class Wypozyczenia(models.Model):
    take_date = models.DateField(null=True, default=date.today, blank=True,verbose_name='Data wypożyczenia')
    take_in = models.DateField(null=True, blank=True, verbose_name='Data zwrotu')
    book = models.ForeignKey(Books, verbose_name='Książka', on_delete=models.CASCADE)
    czytelnik =  models.ForeignKey(Users_take, verbose_name='Czytelnik',  on_delete=models.CASCADE)

    class Meta:
           verbose_name_plural = "Wypożyczenia"
           verbose_name = "Wypożyczenie"

    def __str__(self):
        return self.book.title + str(self.book.number) + self.czytelnik.name

    # def delete_model(self, request, obj):
    #     self.book.available = True
    #     self.delete()

    def save(self, *args, **kwargs):
        if str(self.take_in)=='' or  self.take_in ==  None or  self.take_in is None:
            # if self.take_in <= self.take_date:
            #     raise ValidationError("Błąd daty")
            print('take_in save not None',self.take_in , type(self.take_in))
            print(' przed', self.book.available)

            self.book.available = False
            print(' po', self.book.available)
            self.book.save(*args, **kwargs)
            print(' po ponownie', self.book.available)
        # self.book.save(*args, **kwargs)

        if str(self.take_in) != '' or self.take_in != None:
            print('take_in save  None', self.take_in , type(self.take_in))

            self.book.available = True
        # self.book.save(*args, **kwargs)


        super(Wypozyczenia, self).save(*args, **kwargs)
        if str(self.take_in) == '' or self.take_in == None or self.take_in is None:
            print('available None 1', self.book.available)
            self.book.available = False
            self.book.save(*args, **kwargs)
            print('available None 2', self.book.available)
        # if str(self.take_in) != '' or self.take_in != None or self.take_in is  not None:
        #     print('available',self.book.available)
        #     self.book.available = True
        self.book.save(*args, **kwargs)
        print('available None 3', self.book.available)


