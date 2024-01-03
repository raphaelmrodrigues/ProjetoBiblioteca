from django.shortcuts import render
import datetime
from django.http import HttpResponse
from django.shortcuts import redirect
from usuarios.models import Usuario
from livro.models import Livros, Emprestimos
from .forms import CadastroLivro
from django.db.models import Q


# Create your views here.

def home(request):
    if request.session.get('usuario'):
        livros = Livros.objects.all()
        form = CadastroLivro()
        usuarios = Usuario.objects.all()
        status = request.GET.get('status')
        usuario = Usuario.objects.get(id = request.session['usuario'])
        livros_disponiveis = Livros.objects.filter(emprestado = False)
        livros_emprestados = Livros.objects.filter(emprestado = True)
        total_livros = livros.count()

        return render(request, 'home.html', {'livros': livros,
                                             'usuario_logado': request.session.get('usuario'),
                                             'form': form,
                                             'usuarios': usuarios,
                                             'status': status,
                                             'usuario': usuario,
                                             'livros_disponiveis': livros_disponiveis,
                                             'livros_emprestados': livros_emprestados,
                                             'total_livros': total_livros})
    else:
        return redirect('/auth/login/?status=2')

def ver_livros(request, id):
    if request.session.get('usuario'):
        status = request.GET.get('status')
        livro = Livros.objects.get(id = id)
        form = CadastroLivro()
        usuario = Usuario.objects.get(id = request.session['usuario'])
        livros = Livros.objects.filter(usuario_id = request.session.get('usuario'))
        emprestimos = Emprestimos.objects.filter(livro = livro)
        livros_disponiveis = Livros.objects.filter(emprestado = False)
        livros_emprestados = Livros.objects.filter(emprestado = True)
        return render(request, 'ver_livro.html', {'livro': livro,
                                                  'emprestimos': emprestimos,
                                                  'usuario_logado': request.session.get('usuario'),
                                                  'form': form,
                                                  'usuario':usuario,
                                                  'livros': livros,
                                                  'livros_disponiveis': livros_disponiveis,
                                                  'livros_emprestados': livros_emprestados,
                                                  'status': status})


def cadastrar_livro(request):
    if request.method == 'POST':
        form = CadastroLivro(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('/livro/home/?status=1')
        else:
            return HttpResponse('DADOS INVALIDOS')

def cadastrar_emprestimo(request):
    if request.method == 'POST':
        nome_emprestado = request.POST.get('nome_emprestado')
        livro_emprestado = request.POST.get('livro_emprestado')
        emprestimo = Emprestimos(nome_emprestado_id = nome_emprestado, livro_id = livro_emprestado)
        emprestimo.save()
        livro = Livros.objects.get(id = livro_emprestado)
        livro.emprestado = True
        livro.save()

        return redirect('/livro/home/?status=0')

def devolver_livro(request):
    id = request.POST.get('livro_devolver')
    livro_devolver = Livros.objects.get(id = id)
    emprestimo_devolver = Emprestimos.objects.get(Q(livro = livro_devolver) & Q(data_devolucao = None))
    emprestimo_devolver.data_devolucao = datetime.datetime.now()
    emprestimo_devolver.save()

    livro_devolver.emprestado = False
    livro_devolver.save()

    return redirect('/livro/home/?status=2')

def emprestimos(request):
    usuario = Usuario.objects.get(id = request.session['usuario'])
    emprestimos = Emprestimos.objects.filter(nome_emprestado = usuario)
    livros_disponiveis = Livros.objects.filter(emprestado = False)
    livros_emprestados = Livros.objects.filter(emprestado = True)
    form = CadastroLivro()


    return render(request, 'emprestimos.html', {'usuario_logado': request.session['usuario'],
                                                'emprestimos': emprestimos,
                                                'livros_disponiveis': livros_disponiveis,
                                                'livros_emprestados': livros_emprestados,
                                                'usuario': usuario,
                                                'form': form})

def processa_avaliacao(request):
    if 'id_livro_emprestimo' in request.POST:
        id_livro, id_emprestimo = request.POST['id_livro_emprestimo'].split('_')
    else:
        id_livro = request.POST.get('id_livro')
        id_emprestimo = request.POST.get('id_emprestimo')
    opcoes = request.POST.get('opcoes')
    emprestimo = Emprestimos.objects.get(id = id_emprestimo)
    emprestimo.avaliacao = opcoes
    emprestimo.save()

    return redirect('/livro/emprestimos/?status=0')