from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from usuarios.models import Usuario
from livro.models import Livros, Emprestimos
from .forms import CadastroLivro


# Create your views here.

def home(request):
    if request.session.get('usuario'):
        livros = Livros.objects.all()
        form = CadastroLivro()

        return render(request, 'home.html', {'livros': livros, 'usuario_logado': request.session.get('usuario'), 'form': form})
    else:
        return redirect('/auth/login/?status=2')

def ver_livros(request, id):
    if request.session.get('usuario'):
        livros = Livros.objects.get(id = id)
        form = CadastroLivro()
        emprestimos = Emprestimos.objects.filter(livro = livros)
        return render(request, 'ver_livro.html', {'livro': livros, 'emprestimos': emprestimos, 'usuario_logado': request.session.get('usuario'), 'form': form})

def cadastrar_livro(request):
    if request.method == 'POST':
        form = CadastroLivro(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse
        else:
            return HttpResponse('DADOS INVALIDOS')
