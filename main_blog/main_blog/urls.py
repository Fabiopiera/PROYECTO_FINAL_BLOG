"""
URL configuration for main_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import  path, include
# from .views import index, about, registro  # esto A con A
from django.conf import settings #esta linea agregue
from django.conf.urls.static import static #esta linea agregue
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import IndexView, about, registro, pagina_404

handler404 = pagina_404

urlpatterns = [
    path('admin/', admin.site.urls),
   # path('', index, name='index'), #esto es A
    path('', IndexView.as_view(), name='index'),
    path('about', about, name='about'),
    path('registro', registro, name='registro'),
    path('', include('apps.posts.urls')), # aca declaro la url de mi aplicacion posts
    path('', include('apps.contacto.urls')), # aca declaro la url de mi aplicacion contacto
    path('', include('apps.usuario.urls')), # aca declaro la url de mi aplicacion contacto
    path('', include('django.contrib.auth.urls')), # aca declaro la url de la aplicacion auth
    
    
    
]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#esta linea agregue
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
