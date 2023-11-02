from django.contrib import admin
# from catalogo.models import Genero, Autor, Idioma, Libro, Ejemplar
from catalogo.models import User
from django.contrib.auth.admin import UserAdmin

class UserAdmin(UserAdmin):
    pass
    list_display = ('username', 'first_name', 'last_name', 'image')

admin.site.register(User, UserAdmin)
# admin.site.register(Genero)
# admin.site.register(Autor)
# admin.site.register(Idioma)
# admin.site.register(Libro)
# admin.site.register(Ejemplar)