from django import forms
from .models import Livros

class CadastroLivro(forms.ModelForm):
    class Meta:
        model = Livros
        fields = ('nome', 'autor', 'co_autor', 'data_cadastro', 'emprestado', 'categoria')