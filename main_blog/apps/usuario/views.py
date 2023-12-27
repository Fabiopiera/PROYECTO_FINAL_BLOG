#from django.forms.models import BaseModelForm
#from django.http import HttpResponse
from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from .forms import RegistroUsuarioForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, ListView, DeleteView
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Usuario
from apps.posts.models import Comentario, Post




# Create your views here.

class RegistrarUsuario(CreateView):
    template_name = 'registration/registrar.html'
    form_class = RegistroUsuarioForm
    
    def form_valid(self, form):
        reponse = super().form_valid(form)
        messages.success(self.request, 'Registro exitoso. Por favor inicia sesion.')
        group = Group.objects.get(name= 'Registrado')
        self.object.groups.add(group)
        return redirect('apps.usuario:registrar')
    
class LoginUsuario(LoginView):
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Login exitoso')
        
        return reverse('apps.usuario:login')
    
class LogoutUsuario(LogoutView):
    template_name = 'registration/logout.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Logout exitoso')
        
        return reverse('login')
     
class UsuarioListView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'usuario/usuario_list.html'
    context_object_name = 'usuarios'
    
    def get_queryset(self):
        querySet = super().get_queryset()
        querySet = querySet.exclude(is_superuser = True)
        return querySet
    
class UsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'usuario/eliminar_usuario.html'
    success_url = reverse_lazy('apps.usuario:usuario_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        colaborador_group = Group.objects.get(name= 'Colaborador')
        es_colaborador = colaborador_group in self.object.groups.all()
        context['es_colaborador'] = es_colaborador
        return context
    
    def post(self, request, *args, **kwargs):
        eliminar_comentarios = request.POST.get('eliminar_comentarios', False) 
        eliminar_posts = request.POST.get('eliminar_posts', False)        
        self.object = self.get_object()
        if eliminar_comentarios:
            Comentario.objects.filter(Usuario=self.objects).delete()
            
        if eliminar_posts:
            Post.object.filter(autor=self.object).delete()
        messages.success(request,f'Usuario {self.object.username} eliminado correctamente')
        return self.delete(request, *args,**kwargs)
          
