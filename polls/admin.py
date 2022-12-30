from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Carteira)
admin.site.register(Devolucao)
admin.site.register(Empresa)
admin.site.register(Faturamento)
admin.site.register(Operador)
admin.site.register(LinhaProducao)
admin.site.register(MateriaPrima)
admin.site.register(Minuta)
admin.site.register(PrazoEntrega)
admin.site.register(Relatorio)
admin.site.register(Setor)