from django.shortcuts import render
import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from usuarios.models import Usuario
from livro.models import Livros, Emprestimos
from .forms import CadastroLivro
from django.db.models import Q

from mqtt.main.mqtt_connection.mqtt_cient_connection import MqttClientConnection
from mqtt.configs.broker_configs import mqtt_broker_configs
import time


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
        nome_emprestado = request.POST.get('usuario_id')
        livro_emprestado = request.POST.get('livro_id')

        emprestimo = Emprestimos(nome_emprestado_id = nome_emprestado, livro_id = livro_emprestado)
        emprestimo.save()
        livro = Livros.objects.get(id = livro_emprestado)
        livro.emprestado = True
        livro.save()

        return JsonResponse({'status': 'emprestimo realizado'})

def devolver_livro(request):
    id = request.POST.get('livro_id')
    livro_devolver = Livros.objects.get(id = id)
    emprestimo_devolver = Emprestimos.objects.get(Q(livro = livro_devolver) & Q(data_devolucao = None))
    emprestimo_devolver.data_devolucao = datetime.datetime.now()
    emprestimo_devolver.save()

    livro_devolver.emprestado = False
    livro_devolver.save()

    return JsonResponse({'status': 'devolucao realizada'})

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



def processa_rfid_usuario(request):

    mqtt_client_connection = MqttClientConnection(
        mqtt_broker_configs["HOST"],
        mqtt_broker_configs["PORT"],
        mqtt_broker_configs["CLIENT_NAME"],
        mqtt_broker_configs["KEEPALIVE"]
    )

    mqtt_client_connection.start_connection()


    nome_emprestado = request.POST.get('nome_emprestado')
    livro_emprestado = request.POST.get('livro_emprestado')
    livro = Livros.objects.get(id=livro_emprestado)
    usuario = Usuario.objects.get(id=nome_emprestado)

    while mqtt_client_connection.last_message is None:
        # Aguarde um curto período de tempo antes de verificar novamente
        time.sleep(1)

    if hasattr(mqtt_client_connection, 'last_message'):
        last_message = mqtt_client_connection.last_message
        print(f"Última mensagem recebida: {last_message}")
        if last_message == usuario.idtag:
            mqtt_client_connection.last_message = None
            mqtt_client_connection.end_connection()
            return JsonResponse({'status': 'usuario autenticado', 'usuario_id': usuario.id, 'livro_id': livro.id, 'success': True}, content_type='application/json')

        else:
            mqtt_client_connection.last_message = None
            mqtt_client_connection.end_connection()
            return JsonResponse({'status': 'usuario nao autenticado', 'success': False})

    else:
        print("A instância do MqttClientConnection não foi inicializada ainda.")





def processa_rfid_livro(request):
    mqtt_client_connection = MqttClientConnection(
        mqtt_broker_configs["HOST"],
        mqtt_broker_configs["PORT"],
        mqtt_broker_configs["CLIENT_NAME"],
        mqtt_broker_configs["KEEPALIVE"]
    )
    mqtt_client_connection.start_connection()

    livro_id = request.POST.get('livro_id')
    livro = Livros.objects.get(id=livro_id)

    usuario_id = request.POST.get('usuario_id')
    usuario = Livros.objects.get(id=usuario_id)

    while mqtt_client_connection.last_message is None:
        # Aguarde um curto período de tempo antes de verificar novamente
        time.sleep(1)

    if hasattr(mqtt_client_connection, 'last_message'):
        last_message = mqtt_client_connection.last_message
        print(f"Última mensagem recebida: {last_message}")
        if last_message == livro.idtag:
            mqtt_client_connection.last_message = None
            mqtt_client_connection.end_connection()
            return JsonResponse({'status': 'livro autenticado', 'success': True, 'livro_id': livro.id, 'usuario_id': usuario.id}, content_type='application/json')

        else:
            mqtt_client_connection.last_message = None
            mqtt_client_connection.end_connection()
            return JsonResponse({'status': 'livro nao autenticado', 'success': False})

    else:
        print("A instância do MqttClientConnection não foi inicializada ainda.")

