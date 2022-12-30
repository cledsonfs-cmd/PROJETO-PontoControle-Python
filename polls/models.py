import datetime

from django.db import models

# Create your models here.
class Empresa(models.Model):
    idempresa = models.CharField(max_length=10, null=False, blank=False)
    cnpj = models.CharField(max_length=25, null=False, blank=False)
    nome = models.CharField(max_length=255, null=False, blank=False)
    apelido = models.CharField(max_length=15, null=False, blank=False, default='empresa')
    codigo1 = models.CharField(max_length=10, default='')
    codigo2 = models.CharField(max_length=10, default='')

class Setor(models.Model):
    codigo = models.CharField(max_length=4, null=False, blank=False)
    nome = models.CharField(max_length=25,null=False,blank=False)
    abreviacao = models.CharField(max_length=4, null=False, blank=False)
    idempresa = models.CharField(max_length=10,default='00000')

class Operador(models.Model):
    codigo = models.CharField(max_length=10, null=False, blank=False)
    nome = models.CharField(max_length=25,null=False,blank=False)

class MateriaPrima(models.Model):
    codigo = models.CharField(max_length=10, null=False, blank=False)
    descricao = models.CharField(max_length=25,null=False,blank=False)
    codigo1 = models.CharField(max_length=10, null=True, blank=True)
    codigo2 = models.CharField(max_length=10, null=True, blank=True)

class Relatorio(models.Model):
    codigo = models.CharField(max_length=4, null=False, blank=False)
    descricao = models.CharField(max_length=25, null=False, blank=False)

class Carteira(models.Model):
    data = models.DateField('date published')
    idempresa = models.CharField(max_length=10, null=False, blank=False)
    carteira = models.IntegerField(default=0)

class Minuta(models.Model):
    data = models.DateTimeField('date published')
    idempresa = models.CharField(max_length=10, null=False, blank=False)
    minuta = models.IntegerField(default=0)

class Faturamento(models.Model):
    data = models.DateField('date published')
    idempresa = models.CharField(max_length=10, null=False, blank=False)
    faturamento = models.IntegerField(default=0)

class Devolucao(models.Model):
    idempresa = models.CharField(max_length=10, null=False, blank=False)
    codpedido= models.CharField(max_length=10, null=True, blank=True)
    produto = models.CharField(max_length=100, null=True, blank=True)
    valor = models.FloatField()
    quantidade = models.FloatField()
    unidade= models.CharField(max_length=20, null=True, blank=True)
    data_faturada = models.DateField()
    data_devolucao = models.DateField()
    tipo= models.CharField(max_length=25, null=True, blank=True)
    motivo= models.CharField(max_length=1000, null=True, blank=True)
    representante= models.CharField(max_length=50, null=True, blank=True)
    cliente= models.CharField(max_length=50, null=True, blank=True)
    tempo_devolucao = models.IntegerField(default=0)
    origem_erro= models.CharField(max_length=10, null=True, blank=True)

class LinhaProducao(models.Model):
    descricao = models.CharField(max_length=50, null=True, blank=True)
    codigo1 = models.CharField(max_length=10, null=True, blank=True)
    codigo2 = models.CharField(max_length=10, null=True, blank=True)

class PrazoEntrega(models.Model):
    linhaproducao = models.CharField(max_length=50, null=True, blank=True)
    data = models.DateField()
    prazo = models.FloatField()

class ProducaoSetor(models.Model):
    data = models.DateField()
    produto = models.CharField(max_length=100, null=False, blank=False)
    quantidade = models.FloatField()
    peso = models.FloatField()
    cod_setor = models.CharField(max_length=4, null=True, blank=True)
    maquina = models.CharField(max_length=5, null=True, blank=True)
    cod_processo = models.CharField(max_length=5, null=True, blank=True)
    controlado = models.BooleanField(default=True)

class Processo(models.Model):
    codigo = models.CharField(max_length=5, null=False, blank=False)
    descricao = models.CharField(max_length=50, null=False, blank=False)
    idsetor = models.CharField(max_length=4)

class Reprogramacao(models.Model):
    data = models.DateField()
    idempresa = models.CharField(max_length=10, default='00000')
    idsetor = models.CharField(max_length=4, null=False, blank=False)
    produto = models.CharField(max_length=100,default='')
    retrabalho = models.BooleanField(default=False)
    quantidade = models.FloatField()
    custo = models.FloatField()
    idmotivo = models.IntegerField(default=0)

class Motivo_reprogramacao(models.Model):
    idmotivo = models.IntegerField(default=0)
    descricao = models.CharField(max_length=200, default='')

class Ponto_Controle(models.Model):
    codigo = models.CharField(max_length=4, null=False, blank=False)
    descricao = models.CharField(max_length=200, default='')
    idsetor = models.CharField(max_length=4, null=False, blank=False)
    campos = models.CharField(max_length=1000, default='', null=True)

class Ponto_Controle_Campos(models.Model):
    nome = models.CharField(max_length=15, default='')

    def __str__(self):
        return f'{self.nome}'

class Ponto_Controle_Evento(models.Model):
    codigo_pc = models.CharField(max_length=4, null=False, blank=False)
    data1 = models.DateTimeField(null=True)
    data2 = models.DateTimeField(null=True)
    data3 = models.DateTimeField(null=True)
    produto = models.CharField(max_length=100,null=True)
    quantidade1 = models.FloatField(default=0,null=True)
    quantidade2 = models.FloatField(default=0,null=True)
    quantidade3 = models.FloatField(default=0,null=True)
    peso1 = models.FloatField(default=0,null=True)
    peso2 = models.FloatField(default=0,null=True)
    peso3 = models.FloatField(default=0,null=True)
    valor1 = models.FloatField(default=0,null=True)
    valor2 = models.FloatField(default=0,null=True)
    valor3 = models.FloatField(default=0,null=True)
    observacao1 = models.CharField(max_length=1000,default='',null=True)
    observacao2 = models.CharField(max_length=1000,default='',null=True)
    observacao3 = models.CharField(max_length=1000,default='',null=True)

class SubSetor(models.Model):
    codigo = models.CharField(max_length=4, null=False, blank=False)
    nome = models.CharField(max_length=200, default='')
    idsetor = models.CharField(max_length=4, null=False, blank=False)

class POP(models.Model):
    codigo = models.CharField(max_length=4,default='')
    codsetor = models.CharField(max_length=4,default='')
    codsubsetor = models.CharField(max_length=4,default='')
    revisao = models.IntegerField(default=0)
    data = models.DateTimeField(default=datetime.datetime.now, blank=True)
    responsavel = models.CharField(max_length=250,default='')
    revisor = models.CharField(max_length=250,default='')
    tarefa = models.CharField(max_length=500,default='')
    resultado = models.CharField(max_length=500,default='')
    equipamentos = models.CharField(max_length=1000,default='')
    epi = models.CharField(max_length=1000,default='')
    epc = models.CharField(max_length=1000,default='')
    recomendacao = models.CharField(max_length=1000,default='')
    observacao = models.CharField(max_length=1000,default='')

class Tarefa(models.Model):
    codigo = models.CharField(max_length=4,default='')
    codigo_pop = models.CharField(max_length=4,default='')
    descricao = models.CharField(max_length=500,default='')

class Procedimento(models.Model):
    codigo = models.CharField(max_length=4,default='')
    codigo_tarefa = models.CharField(max_length=4,default='')
    descricao = models.CharField(max_length=1000,default='')
    observacao = models.CharField(max_length=1000,default='')

class FolhaObservacao(models.Model):
    folha = models.CharField(max_length=5, null=True, blank=True)
    cod_processo = models.CharField(max_length=5, null=True, blank=True)
    nome_peca = models.CharField(max_length=100,default='')
    nome_maquina = models.CharField(max_length=100,default='')
    nome_matricula_operador = models.CharField(max_length=200,default='')
    experiencia_servico = models.CharField(max_length=100,default='')
    mestre = models.CharField(max_length=100,default='')
    data = models.DateTimeField(default=datetime.datetime.now, blank=True)
    numero_operacao = models.IntegerField(default=0)
    numero_peca = models.IntegerField(default=0)
    numero_maquina = models.IntegerField(default=0)
    sexo = models.CharField(max_length=25,default='')
    material = models.CharField(max_length=100,default='')
    numero_secao = models.CharField(max_length=25,default='')
    inicio = models.CharField(max_length=25,default='00:00:00')
    fim = models.CharField(max_length=25,default='00:00:00')
    numero_maquinas = models.IntegerField(default=0)

class FolhaElemento(models.Model):
    id_folha = models.IntegerField(default=0)
    ordinal = models.IntegerField(default=0)
    elemento = models.CharField(max_length=100, default='')
    velocidade = models.CharField(max_length=10,default='')
    avanco = models.CharField(max_length=10,default='')

class ElementoTempo(models.Model):
    id_elemento = models.IntegerField(default=0)
    sequencial = models.IntegerField(default=0)
    tempo = models.FloatField()






