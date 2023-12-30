from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('ver_livro/<int:id>', views.ver_livros, name= 'ver_livros'),
    path('cadastrar_livro/', views.cadastrar_livro, name='cadastrar_livro'),
    path('cadastrar_emprestimo/', views.cadastrar_emprestimo, name='cadastrar_emprestimo'),
    path('devolver_livro/', views.devolver_livro, name='devolver_livro'),
    path('emprestimos/', views.emprestimos, name='emprestimos'),
    path('processa_avaliacao', views.processa_avaliacao, name='processa_avaliacao')
]