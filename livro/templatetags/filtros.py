from django import template
from datetime import datetime, timedelta, time

register = template.Library()

@register.filter
def mostra_duracao(value1, value2):
    duracao = value1 - value2
    horas, segundos_restantes = divmod(duracao.seconds, 3600)
    minutos, segundos_finais = divmod(segundos_restantes, 60)

    tempo_formatado = time(int(horas), int(minutos), int(segundos_finais))

    return f"{duracao.days} Dias e {tempo_formatado.strftime('%H:%M:%S')}"
