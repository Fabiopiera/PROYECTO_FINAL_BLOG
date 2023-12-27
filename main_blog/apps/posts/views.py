from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from .models import Post, Categoria
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .forms import ComentarioForm, Comentario, CrearPostForm, Categoria, NuevaCategoriaForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse

 




#Vista basada en clases para la lista de posts
class PostListView(ListView):
    model = Post
    template_name = 'posts/posts.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        querySet = super().get_queryset()
        orden = self.request.GET.get('orden')
        if orden == 'reciente':
            querySet = querySet.order_by('-fecha')
        elif orden == 'antiguo':
            querySet = querySet.order_by('fecha')
        elif orden == 'alfabetico':
            querySet = querySet.order_by('titulo')
        return querySet
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orden'] = self.request.GET.get('orden', 'reciente')
        return context
            
        
    
    
# Vista basada en clases para posts individual   
class PostDetailView(DetailView,LoginRequiredMixin):
    model = Post
    template_name = 'posts/post_individual.html'
    context_object_name = 'posts'
    pk_url_kwarg = "id"
    queryset =Post.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ComentarioForm()
        context['comentarios'] = Comentario.objects.filter(posts_id=self.kwargs['id'])
        return context
    
    def post(self, request, *args, **kwargs):
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.posts_id = self.kwargs['id']
            comentario.save()
            return redirect('apps.posts:post_individual', id=self.kwargs['id'])
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)  
    
class PostPorCategoriaView(ListView):
    model = Post
    template_name = 'posts/posts_por_categoria.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        categoria_id = self.kwargs['pk']
        
        posts = Post.objects.filter(categoria__id=categoria_id)
        
        return posts
    
    # def get_queryset(self):
    #     categoria_id = self.kwargs['pk']
    #     return Post.objects.filter(categoria__id=categoria_id)
    # def get_queryset(self):
    #     return Post.objects.filter(categoria__id=self.kwargs['pk'])
        
             
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CrearPostForm
    template_name = 'posts/crear_post.html'
    success_url = reverse_lazy('apps.posts:posts')
    
class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = NuevaCategoriaForm
    template_name = 'posts/crear_categoria.html'
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('apps.posts:crear_categoria')
        
class CategoriaListView(ListView):
    model = Categoria
    template_name = 'posts/categoria_list.html'
    context_object_name = 'categorias' 
    
class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'posts/categoria_confirm_delete.html'
    success_url = reverse_lazy('apps.posts:categoria_list')   
        
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = CrearPostForm
    template_name = 'posts/modificar_post.html'
    success_url = reverse_lazy('apps.posts:posts')  
    
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/eliminar_post.html'
    success_url = reverse_lazy('apps.posts:posts') 
       
class ComentarioCreateView(LoginRequiredMixin,CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentario/crear_comentario.html'
    #success_url = 'comentario/comentarios'
    success_url = reverse_lazy('apps.comentario:crear_comentario')
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.posts_id = self.kwargs['posts_id']
        return super().form_valid(form) 
    
class  ComentarioUpdateViews(LoginRequiredMixin, UpdateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentario/comentario_form.html'
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('apps.posts:post_individual', args=[self.object.posts.id])
        
class ComentarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Comentario
    template_name = 'comentario/comentario_confirm_delete.html'
    
    def get_success_url(self):
     return reverse('apps.posts:post_individual', args=[self.object.posts.id])
        
