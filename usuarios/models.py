from django.db import models

# Create your models here.

class Usuario(models.Model):
    img = models.ImageField(upload_to='avatar_usuario', null=True, blank=True)
    nome = models.CharField(max_length=30)
    email = models.EmailField()
    senha = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.nome