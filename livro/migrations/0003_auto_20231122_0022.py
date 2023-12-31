# Generated by Django 3.2.23 on 2023-11-22 03:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livro', '0002_auto_20231121_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livros',
            name='data_cadastro',
            field=models.DateField(default=datetime.date(2023, 11, 22)),
        ),
        migrations.AlterField(
            model_name='livros',
            name='data_devolucao',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='livros',
            name='data_emprestimo',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='livros',
            name='nome_emprestado',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='livros',
            name='tempo_duracao',
            field=models.DateField(blank=True, null=True),
        ),
    ]
