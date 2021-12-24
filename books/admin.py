from django.contrib import admin
from .models import Books, Users_take, Kategoria, Klasa,Wypozyczenia
from django.shortcuts import redirect
from import_export import resources
from import_export.admin import ExportMixin


from django.contrib import messages
# admin.site.register(Books)
# admin.site.register(Users_take)
# admin.site.register(Wypozyczenia)

from .models import Books

class BooksResources(resources.ModelResource):
    class Meta:
        model = Books

######################################
#
# def delete_model(ModelAdmin, request, queryset, obj):
#         obj.book.available = True
#         obj.delete()
#         obj.book.available = True
##############################################


class WypozyczeniaAdmin(admin.ModelAdmin):
    list_display = ['czytelnik', 'klasa','book',  'take_date', 'take_in']
    search_fields = ['czytelnik', 'book',  'take_date', 'take_in']
    list_filter = ['czytelnik', 'book',  'take_date', 'take_in']

    # actions = ['delete_model']
    #
    #
    # def delete_model(self, request, obj, queryset):
    #     queryset.update(book__available=True)
    #     queryset.book.available = True
    #     queryset.delete()
    # def make_available(self, request, queryset):
    #     queryset.update(book=True)

    # def delete_model(self, *args, **kwargs):
    #         # self.book.available = True
    #         self.delete(self, *args, **kwargs)
    #         # self.book.available = True
    # actions = [delete_model]

    def klasa(self, obj):
        return obj.czytelnik.klasa_id

    # @admin.register(Car)
    # class CarAdmin(admin.ModelAdmin):
    #     list_display = ('owner', 'color', 'status', 'max_speed',)

    def save_model(self, request, obj, form, change):
            if obj.book.available==False and obj.take_in is  None:
                messages.add_message(request, messages.ERROR, f'Książka niedostępna {obj.book.title} nr {obj.book.number}')
                messages.add_message(request, messages.INFO, f'Książka wypożyczona {obj.book.title} nr {obj.book.number}')
                return redirect('/admin/books/books/')

            if obj.take_in is not None:
                obj.book.available = True

                # super(WypozyczeniaAdmin, self).save_model(request, obj, form, change)
            super(WypozyczeniaAdmin, self).save_model(request, obj, form, change)

    def response_change(self, request, obj):
        if obj.book.available == False :
            messages.add_message(request, messages.ERROR, f'Książka niedostępna {obj.book.title} nr {obj.book.number}')
            return redirect('/admin/books/books/')
        else:
            return redirect('/admin/books/wypozyczenia/')

    def response_add(self, request, obj):
        if obj.book.available == False:
            messages.add_message(request, messages.ERROR, f'Książka niedostępna {obj.book.title} nr {obj.book.number}')
            messages.add_message(request, messages.INFO, f'Książka wypożyczona {obj.book.title} nr {obj.book.number}')
            return redirect('/admin/books/books/')
            if obj.book.available == True:
                # messages.add_message(request, messages.INFO, f'Książka wypożyczona {obj.book.title}')
                return redirect('/admin/books/wypozyczenia/')

    def response_delete(self, request,obj,  obj_display, obj_id,form, change):
            print(' obj.book.available',  obj.book.available)
            obj.book.available = True
            obj.book.save()
            super(WypozyczeniaAdmin, self).response_delete(request, obj, form, change)
            obj.book.save()


    # def delete_model(self, request, obj):
    #     obj.book.available = True
    #     obj.delete()
    #     obj.book.available = True
    #     return obj.book.save()

    # def dostepnosc(self, obj):
    #     return obj.book.available





class BooksAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['title',  'publicated_year',  'author_family',
                    'author_name' ,'number','available', 'image_tag', 'image']
    search_fields = ['title', 'publicated_year',  'author_family',  'author_name' ]
    list_filter = ['title',  'publicated_year', 'author_family', 'author_name','available']
    resources_class = BooksResources

    actions = ['make_available']

    def make_available(self, request, queryset):
        queryset.update(available=True)

    make_available.short_description = "Ustaw dostępność"

    # def get_actions(self, request):
    #     actions = super(BooksAdmin, self).get_actions(request)
    #     del actions['delete_selected']
    #     return actions
    #
    # def delete_model(self, request, obj):
    #     for o in obj.all():
    #         Wypozyczenia.objects.filter(invoice=o).update(available=True)
    #         o.delete()
    #

class KategoriaAdmin(admin.ModelAdmin):

    search_fields = ['title_kat']
    list_filter = ['title_kat']


class Users_takeAdmin(admin.ModelAdmin):
    list_display = ['name', 'family','klasa_id' ]
    search_fields = ['name', 'family','klasa_id' ]
    list_filter = ['name', 'family','klasa_id']



class KlasaAdmin(admin.ModelAdmin):

    search_fields = ['name']
    list_filter = ['name']


admin.site.register(Books, BooksAdmin) # rozszerzenie klasy Books
admin.site.register(Kategoria, KategoriaAdmin)
admin.site.register(Users_take, Users_takeAdmin)
admin.site.register(Klasa, KlasaAdmin)
admin.site.register(Wypozyczenia, WypozyczeniaAdmin)

# def delete_model(modeladmin, request, queryset):
#     for obj in queryset:
#         filename=obj.profile_name+".xml"
#         os.remove(os.path.join(obj.type,filename))
#         obj.delete()