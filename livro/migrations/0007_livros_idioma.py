# Generated by Django 3.2.23 on 2023-11-27 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livro', '0006_alter_livros_data_cadastro'),
    ]

    operations = [
        migrations.AddField(
            model_name='livros',
            name='idioma',
            field=models.CharField(choices=[('PT-BR', 'Portugues-BR'), ('EN-US', 'Ingles (Estados Unidos)'), ('FR', 'Frances'), ('ES', 'Espanhol')], default='PT=BR', max_length=30),
        ),
    ]
