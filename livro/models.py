from django.db import models
from datetime import date
import datetime
from usuarios.models import Usuario

# Create your models here.

class Categoria(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.TextField()

    def __str__(self):
        return self.nome



class Livros(models.Model):
    img = models.ImageField(upload_to='capa_livro', null=True, blank=True)
    nome = models.CharField(max_length = 100)
    autor = models.CharField(max_length = 30)
    co_autor = models.CharField(max_length = 30, blank=True)
    data_cadastro = models.DateField(default=date.today())
    editora = models.CharField(max_length = 60, blank=True, null=True)
    data_publicacao = models.DateField(default=date.today())
    numero_paginas = models.IntegerField(blank=True, null=True)
    edicao = models.IntegerField(default = 1)
    i = (
        ('PT-BR', 'Portugues-BR'),
        ('EN-US', 'Ingles (Estados Unidos)'),
        ('FR', "Frances"),
        ('ES', "Espanhol"),
    )
    idioma = models.CharField(max_length=30, choices=i, default='PT-BR')
    descricao = models.TextField(blank=True, null=True)
    emprestado = models.BooleanField(default=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank=True, null=True)


    class Meta:
        verbose_name = 'Livro'

    def __str__(self):
        return self.nome


class Emprestimos(models.Model):
    choices = (
        ('P', 'Pessimo'),
        ('R', 'Ruim'),
        ('RL', 'Regular'),
        ('B', 'Bom'),
        ('O', 'Ótimo')
    )
    nome_emprestado = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    data_emprestimo = models.DateTimeField(default=datetime.datetime.now())
    data_devolucao = models.DateTimeField(blank=True, null=True)
    livro = models.ForeignKey(Livros, on_delete=models.DO_NOTHING)
    avaliacao = models.CharField(max_length=15, choices=choices, null=True, blank=True)



    class Meta:
        verbose_name = 'Emprestimo'

    def __str__(self):
        return f"{self.nome_emprestado} | {self.livro}"



