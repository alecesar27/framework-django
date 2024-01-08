from typing import Any
from django.http import HttpResponse
from django.shortcuts import render , redirect, reverse
from django.views.generic import TemplateView, ListView, DetailView ,FormView, UpdateView
from .forms import CriarContaForm, FormHomePage

from .models import Filme , Usuario
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class Homepage(FormView):
    
    template_name = "homepage.html"
    form_class= FormHomePage
    
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
          return redirect('filme:homefilmes')       #redireciona para home filmes
        else:        
            return super().get(self, request, *args, **kwargs)   
        
        
    def get_success_url(self):
        
        email= self.request.POST.get('email')
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            return reverse('filme:login')
        else:
            return reverse('filme:criarConta')
    
# sempre tem que criar url -view -html


class Homefilmes(LoginRequiredMixin,ListView):
    template_name = "homefilmes.html"
    # object list não uma lista já tem tudo pronto no ListView
    model = Filme  # lista de items do modelo


class DetalhesFilme(LoginRequiredMixin,DetailView):
    template_name = "detalhesfilme.html"
    model = Filme  # lista do nosso modelo

    def get(self, request, *args, **kwargs):

        # precisa descobrir que filme o usuario está acessando
        # somar um às visualizações do filme
        filme = self.get_object()
        filme.visualizacoes += 1
        filme.save()
        usuario = request.user
        usuario.filmes_vistos.add(filme)
        
        # redireciona o usuário para o link final
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DetalhesFilme, self).get_context_data(**kwargs)
        # filtrar a tabela de filmes e pegar os filmes cuja categoria seja programacao (object)
        # self.get_object()
        filmes_relacionados = Filme.objects.filter(
            categoria=self.get_object().categoria)  # [0:5] limita a no máximo trazer 5 filmes
        context['filmes_relacionados'] = filmes_relacionados
        return context
    
class PesquisaFilme(LoginRequiredMixin,ListView):
    template_name = "pesquisa.html"
    model = Filme  # lista do nosso modelo
    
    
    #object_list faz o filtro da caixa de pesquisa
    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = Filme.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            
            return None
        


class PaginaPerfil(LoginRequiredMixin,UpdateView):
        
    template_name = "editarPerfil.html"
    model = Usuario
    fields = ['first_name','last_name','email']
    
    def get_success_url(self):
        return reverse('filme:homefilmes')
    
    
    
class CriarConta(FormView):
        
    template_name = "criarConta.html"  
    
    form_class = CriarContaForm  
    
    def form_valid(self, form):
        form.save()  #aqui que efetivamente cria o usuário no banco
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('filme:login') #usa reverse quando espera um texto de um link  pois o redirect não funciona
    
    
# Fazendo com function
# def homepage(request):
#    return render(request, "homepage.html")

# fazendo com function
# def homefilmes(request):
#    context = {}
#    lista_filmes = Filme.objects.all()
#    context['lista_filmes'] = lista_filmes
#    return render(request, "homefilmes.html", context)
