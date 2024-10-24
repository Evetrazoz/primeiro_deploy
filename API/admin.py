from django.contrib import admin

# Register your models here.
from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'publicado_em',)
    list_display_links = ('titulo',)
    list_filter = ('titulo','autor')
    search_fields = ('titulo',)
    list_editable = ('autor',) #nao pode coincidir com o display_links