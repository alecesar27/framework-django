# url - view - template

from django.urls import path, reverse_lazy
from .views import Homefilmes, Homepage, DetalhesFilme, PesquisaFilme, PaginaPerfil, CriarConta
from django.contrib.auth import views as auth_view
# fazer essa importacao

app_name = 'filme'

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('filmes/', Homefilmes.as_view(), name='homefilmes'),
    path('filmes/<int:pk>', DetalhesFilme.as_view(), name='detalhesfilme'),
    path('pesquisa/',PesquisaFilme.as_view(),name='pesquisafilme'),
    path('login',auth_view.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout',auth_view.LogoutView.as_view(template_name='logout.html'),name='logout'),
    path('editarPerfil/<int:pk>',PaginaPerfil.as_view(),name='editarPerfil'),
    path('criarConta',CriarConta.as_view(),name='criarConta'),
    path('mudarSenha/', auth_view.PasswordChangeView.as_view(template_name='editarPerfil.html',
                                                             success_url=reverse_lazy('filme:homefilmes')),name='mudarSenha'),
    
]
