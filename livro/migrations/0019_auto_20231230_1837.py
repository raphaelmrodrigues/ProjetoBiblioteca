# Generated by Django 3.2.23 on 2023-12-30 21:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
        ('livro', '0018_alter_emprestimos_data_emprestimo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='avaliacoes',
            options={'verbose_name': 'Avaliacoe'},
        ),
        migrations.AddField(
            model_name='avaliacoes',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='usuarios.usuario'),
        ),
        migrations.AlterField(
            model_name='emprestimos',
            name='data_emprestimo',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 30, 18, 37, 24, 989026)),
        ),
    ]