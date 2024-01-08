from django.contrib.auth.forms import UserCreationForm
from.models import Usuario
from django import forms 

class FormHomePage(forms.Form): #Usa o formulario padrao do django
    
    email = forms.EmailField(label=False)

#necessario para criar o formulario personalizado
class CriarContaForm(UserCreationForm):
    
    email = forms.EmailField()
    
    # o nome desses campos são obrigatórios para a criação do formulário do usuario
    class Meta:
        model = Usuario
        fields =('username','email', 'password1','password2') 