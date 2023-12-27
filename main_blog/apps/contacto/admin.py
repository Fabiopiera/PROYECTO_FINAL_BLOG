from django.contrib import admin
from .models import Contacto

# Register your models here.

@admin.register(Contacto)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_apellido', 'email', 'asunto', 'mensaje', 'fecha')
    #list_editable = ('asunto',)
    #list_editable = ('mensaje',)