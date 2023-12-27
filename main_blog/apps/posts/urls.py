from django.urls import path
#from .views import PostListView, PostDetailView, PostCreateView, CategoriaCreateView
from .views import *

app_name = 'apps.posts'

urlpatterns = [
    path("posts/", PostListView.as_view(), name='posts'),
    path("posts/<int:id>/", PostDetailView.as_view(), name='post_individual'),
    path("crear_posts/", PostCreateView.as_view(), name='crear_post'),
    path("posts/categoria/", CategoriaCreateView.as_view(), name='crear_categoria'),
    path("categoria/", CategoriaListView.as_view(), name='categoria_list'),
    path("categoria/<int:pk>/delete/", CategoriaDeleteView.as_view(), name='categoria_delete'), #-------
    path("categoria/<int:pk>/posts/", PostPorCategoriaView.as_view(), name='posts_por_categoria'),
    
    path("post/<int:pk>/modificar/", PostUpdateView.as_view(), name='post_update'), #-------
    path("post/<int:pk>/eliminar/", PostDeleteView.as_view(), name='post_delete'),
    path("comentario/<int:pk>/editar/", ComentarioUpdateViews.as_view(), name='comentario_editar'),
    path("comentario/<int:pk>/eliminar/", ComentarioDeleteView.as_view(), name='comentario_confirm_delete'),
    path("comentario/<int:posts_id>/crear/", ComentarioCreateView.as_view(), name='crear_comentario'),
    
    
    
    
    
]

