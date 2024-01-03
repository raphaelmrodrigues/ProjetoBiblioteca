from django import forms
from .models import Livros
from .models import Emprestimos

class CadastroLivro(forms.ModelForm):
    class Meta:
        model = Livros
        fields = ('img', 'nome', 'autor', 'co_autor', 'editora', 'data_publicacao', 'numero_paginas', 'edicao', 'idioma', 'descricao',
                 'emprestado', 'categoria', 'usuario')
