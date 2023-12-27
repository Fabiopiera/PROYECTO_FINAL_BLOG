from django.urls import path
from .views import ContactoUsuario


app_name = 'apps.contacto'

urlpatterns = [
    path('contacto/', ContactoUsuario.as_view(), name= 'contacto')
]
