import datetime

from django.contrib.auth.models import User,Group, GroupManager
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import QuerySet
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'

def salvarTempo(_id,_sequencial,_tempo):
    obj = ElementoTempo()
    obj.id_elemento = _id
    obj.sequencial = _sequencial
    obj.tempo = _tempo
    return  obj

#forms inserção
class CarteiraForm(ModelForm):
    class Meta:
        model = Carteira
        fields = ['idempresa', 'carteira', 'data']

    empresa_list = Empresa.objects.raw('select id,nome from polls_empresa')
    lista_e = []
    for obj in empresa_list:
        lista_e.append((obj.idempresa, obj.nome))

    idempresa = forms.CharField(label='Empresa', widget=forms.Select(choices=lista_e,attrs={'class': 'form-control form-control-sm','data-toggle': 'dropdown'}))
    carteira =forms.IntegerField(label='Valor',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0'}))
    data = forms.DateField(label='Data',initial=datetime.datetime.now(),widget=DateInput(attrs={'class': 'form-control'}))

    def save(self):
        _CarteiraForm = super(CarteiraForm, self).save(commit=False)
        _CarteiraForm.save()
        return _CarteiraForm

class DevolucaoForm(ModelForm):
    class Meta:
        model = Devolucao
        fields = ['idempresa'
            ,'codpedido'
            ,'produto'
            ,'valor'
            ,'quantidade'
            ,'unidade'
            ,'data_faturada'
            ,'data_devolucao'
            ,'tipo'
            ,'motivo'
            ,'representante'
            ,'cliente'
            ,'tempo_devolucao'
            ,'origem_erro']

    empresa_list = Empresa.objects.raw('select id,nome from polls_empresa')
    lista_e = []
    for obj in empresa_list:
        lista_e.append((obj.idempresa, obj.nome))

    lista_t = []
    lista_t.append(('DEVOLUÇÃO', 'Devolução'))
    lista_t.append(('CONCERTO', 'Concerto'))

    lista_o = []
    lista_o.append(('CLIENTE', 'Cliente'))
    lista_o.append(('FABRICA', 'Fabrica'))
    lista_o.append(('REPRESENTANTE', 'Representante'))

    idempresa = forms.CharField(label='Empresa', widget=forms.Select(choices=lista_e,attrs={'class': 'form-control form-control-sm','data-toggle': 'dropdown'}))
    codpedido = forms.CharField(label='Codigo do Pedido',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10 Caracteres'}))
    produto = forms.CharField(label='Produto',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '100 Caracteres'}))
    valor = forms.FloatField(label='Valor',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0'}))
    quantidade = forms.FloatField(label='Quantidade',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0'}))
    unidade = forms.CharField(label='Unidade',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '20 Caracteres'}))
    data_faturada = forms.DateField(label='Data Faturamento',initial=datetime.datetime.now(),widget=DateInput(attrs={'class': 'form-control'}))
    data_devolucao = forms.DateField(label='Data Devolução',initial=datetime.datetime.now(),widget=DateInput(attrs={'class': 'form-control'}))
    tipo = forms.CharField(label='Tipo', widget=forms.Select(choices=lista_t,attrs={'class': 'form-control'}))
    motivo = forms.CharField(label='Motivo',widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '1000 Caracteres'}))
    representante = forms.CharField(label='Representante',widget=forms.TextInput(attrs={'class': 'form-control','size':'55', 'placeholder': '50 Caracteres'}))
    cliente = forms.CharField(label='Cliente',widget=forms.TextInput(attrs={'class': 'form-control','size':'55', 'placeholder': '50 Caracteres'}))
    tempo_devolucao = forms.CharField(label='Tempo da Devolucao',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0'}))
    origem_erro = forms.CharField(label='Origem do Erro', widget=forms.Select(choices=lista_o,attrs={'class': 'form-control'}))

    def save(self):
        _DevolucaoForm = super(DevolucaoForm, self).save(commit=False)
        _DevolucaoForm.save()
        return _DevolucaoForm

class FaturamentoForm(ModelForm):
    class Meta:
        model = Faturamento
        fields = ['idempresa', 'faturamento', 'data']

    empresa_list = Empresa.objects.raw('select id,nome from polls_empresa')
    lista_e = []
    for obj in empresa_list:
        lista_e.append((obj.idempresa, obj.nome))

    idempresa = forms.CharField(label='Empresa', widget=forms.Select(choices=lista_e,attrs={'class': 'form-control form-control-sm','data-toggle': 'dropdown'}))
    data = forms.DateField(label='Data',initial=datetime.datetime.now(),widget=DateInput(attrs={'class': 'form-control'}))
    faturamento = forms.FloatField(label='Valor',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0'}))

    def save(self):
        _FaturamentoForm = super(FaturamentoForm, self).save(commit=False)
        _FaturamentoForm.save()
        return _FaturamentoForm

class PrazoEntregaForm(ModelForm):
    class Meta:
        model = PrazoEntrega
        fields = ['linhaproducao', 'data', 'prazo']

    linha_producao_list = LinhaProducao.objects.order_by('descricao')
    lista_e = []
    for obj in linha_producao_list:
        lista_e.append((obj.codigo1, obj.descricao))

    linhaproducao = forms.CharField(label='Linha de Produção', widget=forms.Select(choices=lista_e,attrs={'class': 'form-control form-control-sm','data-toggle': 'dropdown'}))
    data = forms.DateField(label='Data',initial=datetime.datetime.now(),widget=DateInput(attrs={'class': 'form-control'}))
    prazo = forms.FloatField(label='Prazo',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0'}))

    def save(self):
        _PrazoEntregaForm = super(PrazoEntregaForm, self).save(commit=False)
        _PrazoEntregaForm.save()
        return _PrazoEntregaForm

class ProducaoSetorForm(ModelForm):
    class Meta:
        model =ProducaoSetor
        fields = ['data'
            ,'produto'
            ,'quantidade'
            ,'peso'
            #,'cod_setor'
            ,'maquina'
            ,'cod_processo'
            ,'controlado']

    setor_list = Setor.objects.order_by('nome')
    lista_s = []
    for obj in setor_list:
            lista_s.append((obj.codigo, obj.nome))

    lista_c = []
    lista_c.append((True,'Sim'))
    lista_c.append((False,'Não'))

    data = forms.DateField(label='Data Produção',initial=datetime.datetime.now(),widget=DateInput(attrs={'class': 'form-control'}))
    #cod_setor = forms.CharField(label='Setor', widget=forms.Select(choices=lista_s))
    produto = forms.CharField(label='Produto',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '100 Caracteres'}))
    quantidade = forms.FloatField(label='Quantidade',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0'}))
    peso = forms.FloatField(label='Peso',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0'}))
    maquina = forms.CharField(label='Maquina',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '5 Caracteres'}))
    cod_processo = forms.CharField(label='Processo',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '5 Caracteres'}))
    controlado = forms.CharField(label='Controla OP', widget=forms.Select(choices=lista_c,attrs={'class': 'form-control form-control-sm','data-toggle': 'dropdown'}))


    def save(self,id):
        _ProducaoSetorForm = super(ProducaoSetorForm, self).save(commit=False)
        _ProducaoSetorForm.cod_setor = id
        _ProducaoSetorForm.save()
        return _ProducaoSetorForm

    def update(self):
        _ProducaoSetorForm = super(ProducaoSetorForm, self).save(commit=False)
        _ProducaoSetorForm.save()
        return _ProducaoSetorForm

class ReprogramacaoForm(ModelForm):
    class Meta:
        model = Reprogramacao
        fields = ['data'
            ,'idempresa'
            ,'idsetor'
            ,'produto'
            ,'retrabalho'
            ,'quantidade'
            ,'custo'
            ,'idmotivo']

    empresa_list = Empresa.objects.raw('select id,nome from polls_empresa')
    lista_e = []
    for obj in empresa_list:
        lista_e.append((obj.idempresa, obj.nome))

    setor_list = Setor.objects.order_by('nome')
    lista_s = []
    for obj in setor_list:
            lista_s.append((obj.codigo, obj.nome))

    motivo_list = Motivo_reprogramacao.objects.order_by('descricao')
    lista_m = []
    for obj in motivo_list:
        lista_m.append((obj.idmotivo, obj.descricao))

    lista_r = []
    lista_r.append((False,'Reprogramação'))
    lista_r.append((True,'Retrabalho'))

    data = forms.DateField(label='Data',initial=datetime.datetime.now(),widget=DateInput(attrs={'class': 'form-control'}))
    idempresa = forms.CharField(label='Empresa', widget=forms.Select(choices=lista_e,attrs={'class': 'form-control form-control-sm','data-toggle': 'dropdown'}))
    idsetor = forms.CharField(label='Empresa', widget=forms.Select(choices=lista_s,attrs={'class': 'form-control form-control-sm','data-toggle': 'dropdown'}))
    produto = forms.CharField(label='Produto',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '100 Caracteres'}))
    retrabalho = forms.CharField(label='Empresa', widget=forms.Select(choices=lista_r,attrs={'class': 'form-control form-control-sm','data-toggle': 'dropdown'}))
    quantidade = forms.FloatField(label='Quantidade',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0'}))
    custo = forms.FloatField(label='Custo',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0'}))
    idmotivo = forms.CharField(label='Empresa', widget=forms.Select(choices=lista_m,attrs={'class': 'form-control form-control-sm','data-toggle': 'dropdown'}))


    def save(self):
        _ReprogramacaoForm = super(ReprogramacaoForm, self).save(commit=False)
        _ReprogramacaoForm.save()
        return _ReprogramacaoForm

class PontoControleEventoForm(ModelForm):
    class Meta:
        model = Ponto_Controle
        fields = ['codigo', 'inicio', 'fim', 'produto', 'quantidade', 'peso', 'valor', 'observacao']

    codigo =  forms.CharField(label='Código')
    inicio = forms.DateField(label='Inicio',initial=datetime.datetime.now(),widget=DateInput)
    fim = forms.DateField(label='Fim',initial=datetime.datetime.now(),widget=DateInput)
    produto = forms.CharField(label='Nome')
    quantidade =  forms.FloatField(label='Quantidade')
    peso = forms.FloatField(label='Peso')
    valor =  forms.FloatField(label='Valor')
    observacao =  forms.CharField(label='Observação')


    def save(self):
        _PontoControleForm = super(PontoControleForm, self).save(commit=False)
        _PontoControleForm.save()
        return _PontoControleForm

#forms cadastros
class UsuarioForm(UserCreationForm):

    grupos = Group.objects.all();

    username = forms.CharField(label='Login',required=True ,widget=forms.TextInput(attrs={'class': 'form-control','value':''}))
    password1 = forms.CharField(label='Senha',required=True ,widget=forms.PasswordInput(attrs={'class': 'form-control','value':''}))
    password2 = forms.CharField(label='Repita a Senha',required=True ,widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    first_name = forms.CharField(label='Nome',required=True ,widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Ultimo Nome',required=True ,widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Email',required=False ,widget=forms.TextInput(attrs={'class': 'form-control'}))
    idgrupo = forms.CharField(label='Setor', widget=forms.Select(choices=grupos.values_list(),attrs={'class': 'btn btn-secondary dropdown-toggle dropdown-toggle-split','data-toggle': 'dropdown'}))

    def save(self,first_name,last_name,email,idgrupo,password):
        _UsuarioForm = super(UsuarioForm,self).save(commit=False)
        user = User.objects.create_user(_UsuarioForm.username, email, password)
        user.is_superuser = False
        user.is_staff = False
        user.is_active = True
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        group = Group.objects.get(pk=idgrupo)
        group.user_set.add(user)
        group.save()

class EmpresaForm(ModelForm):
    class Meta:
        model = Empresa
        fields = ['idempresa', 'cnpj','nome','apelido','codigo1','codigo2']

    idempresa = forms.CharField(label='Código Empresa',required=True ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000' }))
    cnpj= forms.CharField(label='CNPJ', required=True,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000/0000-00'}))
    nome = forms.CharField(label='Razão Social', required=True,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '255 Caracteres'}))
    apelido = forms.CharField(label='Nome Fantasia',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '15 Caracteres'}))
    codigo1 = forms.CharField(label='Código 1',required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10 Caracteres (Opcional)'}))
    codigo2 = forms.CharField(label='Código 2',required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10 Caracteres (Opcional)'}))

    def save(self):
        _EmpresaForm = super(EmpresaForm, self).save(commit=False)
        _EmpresaForm.save()
        return _EmpresaForm

class LinhaProducaoForm(ModelForm):
    class Meta:
        model = LinhaProducao
        fields = ['descricao','codigo1','codigo2']

    descricao= forms.CharField(label='Nome',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "50 Caracteres"}))
    codigo1 = forms.CharField(label='Código 1',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "10 Caracteres"}))
    codigo2 = forms.CharField(label='Código 2',required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "10 Caracteres (Opcional)"}))

    def save(self):
        _LinhaProducaoForm = super(LinhaProducaoForm, self).save(commit=False)
        _LinhaProducaoForm.save()
        return _LinhaProducaoForm

class MateriaPrimaForm(ModelForm):
    class Meta:
        model = MateriaPrima
        fields = ['codigo','descricao','codigo1','codigo2']

    codigo = forms.CharField(label='Codigo',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "0000000000"}))
    descricao = forms.CharField(label='Descrição',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "25 Caracteres"}))
    codigo1 = forms.CharField(label='Código 1',required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "10 Caracteres (Opcional)"}))
    codigo2 = forms.CharField(label='Código 2',required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "10 Caractreres (Opcional)"}))

    def save(self):
        _MateriaPrimaForm = super(MateriaPrimaForm, self).save(commit=False)
        _MateriaPrimaForm.save()
        return _MateriaPrimaForm

class OperadorForm(ModelForm):
    class Meta:
        model = Operador
        fields = ['codigo','nome']

    codigo = forms.CharField(label='Codigo',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "0000000000"}))
    nome = forms.CharField(label='Nome',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "25 Caracteres"}))

    def save(self):
        _OperadorForm = super(OperadorForm, self).save(commit=False)
        _OperadorForm.save()
        return _OperadorForm

class ProcessoForm(ModelForm):
    class Meta:
        model = Processo
        fields = ['codigo','descricao','idsetor']

    setor_list = Setor.objects.all().order_by('nome')
    lista_e = []
    for obj in setor_list:
        lista_e.append((obj.codigo, obj.nome))

    codigo = forms.CharField(label='Codigo',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000' }))
    descricao = forms.CharField(label='Nome',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '50 Caracteres'}))
    idsetor = forms.CharField(label='Setor', widget=forms.Select(choices=lista_e,attrs={'class': 'btn btn-secondary dropdown-toggle dropdown-toggle-split','data-toggle': 'dropdown'}))

    def save(self):
        _ProcessoForm = super(ProcessoForm, self).save(commit=False)
        _ProcessoForm.save()
        return _ProcessoForm

class MotivoReprogramacaoForm(ModelForm):
    class Meta:
        model = Motivo_reprogramacao
        fields = ['idmotivo','descricao']

    idmotivo = forms.CharField(label='Código',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "0"}))
    descricao= forms.CharField(label='Descrição',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "200 Caracteres"}))

    def save(self):
        _MotivoReprogramacaoForm = super(MotivoReprogramacaoForm, self).save(commit=False)
        _MotivoReprogramacaoForm.save()
        return _MotivoReprogramacaoForm

class SetorForm(ModelForm):
    class Meta:
        model = Setor
        fields = ['codigo', 'nome','abreviacao','idempresa']

    empresa_list = Empresa.objects.raw('select id,idempresa,nome from polls_empresa')
    lista_e = []
    for obj in empresa_list:
        lista_e.append((obj.idempresa, obj.nome))

    codigo = forms.CharField(label='Código',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0000'}))
    nome = forms.CharField(label='Nome',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '25 Caracteres'}))
    abreviacao = forms.CharField(label='Abreviação',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '4 Caracteres'}))
    idempresa = forms.CharField(label='Empresa', widget=forms.Select(choices=lista_e,attrs={'class': 'btn btn-secondary dropdown-toggle dropdown-toggle-split','data-toggle': 'dropdown'}))

    def save(self):
        _SetorForm = super(SetorForm, self).save(commit=False)
        _SetorForm.save()
        return _SetorForm

class SubSetorForm(ModelForm):
    class Meta:
        model = SubSetor
        fields = ['codigo','nome','idsetor']

    setor_list = Setor.objects.raw('select '
                                   's.codigo,'
                                   '(CASE'
                                   ' when e.apelido is null THEN s.nome '
                                   'ELSE '
                                   '	s.nome||\' (\' || e.apelido||\')\' '
                                   'END) as nome,s.id '
                                   'from polls_setor as s '
                                   'left join polls_empresa e on e.idempresa=s.idempresa',
                                   translations={'id':'id', 'codigo': 'codigo', 'nome':'nome'})
    lista_e = []
    for obj in setor_list:
        lista_e.append((obj.codigo, obj.nome))

    codigo = forms.CharField(label='Código',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0000'}))
    nome= forms.CharField(label='Descrição',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '200 Caracteres'}))
    idsetor = forms.CharField(label='Setor', widget=forms.Select(choices=lista_e,attrs={'class': 'btn btn-secondary dropdown-toggle dropdown-toggle-split','data-toggle': 'dropdown'}))


    def save(self):
        _SubSetorForm = super(SubSetorForm, self).save(commit=False)
        _SubSetorForm.save()
        return _SubSetorForm

class PontoControleForm(ModelForm):
    class Meta:
        model = Ponto_Controle
        fields = ['codigo','descricao', 'idsetor','campos']
    campos = Ponto_Controle_Campos.objects.all().order_by('nome');
    setor_list = Setor.objects.raw('select '
                                   's.codigo,'
                                   '(CASE'
                                   ' when e.apelido is null THEN s.nome '
                                   'ELSE '
                                   '	s.nome||\' (\' || e.apelido||\')\' '
                                   'END) as nome,s.id '
                                   'from polls_setor as s '
                                   'left join polls_empresa e on e.idempresa=s.idempresa',
                                   translations={'id': 'id', 'codigo': 'codigo', 'nome': 'nome'})

    lista_e = []
    for obj in setor_list:
        lista_e.append((obj.codigo, obj.nome))

    codigo =  forms.CharField(label='Código', widget=forms.TextInput(attrs={'readonly':'readonly','class': 'form-control', 'placeholder': 'Enter Código'}))
    descricao =  forms.CharField(label='Nome',widget=forms.TextInput(attrs={'size':'55','class': 'form-control', 'placeholder': '200 Caracteres'}))
    idsetor = forms.CharField(label='Setor', widget=forms.Select(choices=lista_e,attrs={'class': 'form-control form-control-sm','data-toggle': 'dropdown'}))
    campos = forms.ModelMultipleChoiceField(
        widget = forms.CheckboxSelectMultiple(),
        queryset = Ponto_Controle_Campos.objects.all())


    def save(self):
        _PontoControleForm = super(PontoControleForm, self).save(commit=False)
        _PontoControleForm.save()
        return _PontoControleForm

class PopForm(ModelForm):
    class Meta:
        model = POP
        fields = ['codigo','codsetor','codsubsetor','revisao','responsavel','revisor','tarefa','resultado','equipamentos','epi',
                  'epc','recomendacao','observacao']

    setor_list = Setor.objects.raw('select '
                                   's.codigo,'
                                   '(CASE'
                                   ' when e.apelido is null THEN s.nome '
                                   'ELSE '
                                   '	s.nome||\' (\' || e.apelido||\')\' '
                                   'END) as nome,s.id '
                                   'from polls_setor as s '
                                   'left join polls_empresa e on e.idempresa=s.idempresa',
                                   translations={'id': 'id', 'codigo': 'codigo', 'nome': 'nome'})
    lista_e = []
    for obj in setor_list:
        lista_e.append((obj.codigo, obj.nome))

    subsetor_list = SubSetor.objects.all().order_by('nome')
    lista_e1 = []
    for obj in subsetor_list:
        lista_e1.append((obj.codigo, obj.nome))

    codigo = forms.CharField(label='Código' ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0000' }))
    codsetor = forms.CharField(label='Setor', widget=forms.Select(choices=lista_e,attrs={'class': 'form-control form-control-sm','data-toggle': 'dropdown'}))
    codsubsetor = forms.CharField(label='Sub-Setor', widget=forms.Select(choices=lista_e1,attrs={'class': 'form-control form-control-sm','data-toggle': 'dropdown'}),required=False)
    revisao = forms.IntegerField(label='Revisão' ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0' }))
    responsavel = forms.CharField(label='Responsável' ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '250 Caracteres' }))
    revisor = forms.CharField(label='Revisor' ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '250 Caracteres' }))
    tarefa = forms.CharField(label='Tarefa' ,widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '500 Caracteres','rows':'3' }))
    resultado = forms.CharField(label='Resultado',required=False ,widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '500 Caracteres', 'rows':'3' }))
    equipamentos = forms.CharField(label='Equipamentos',required=False ,widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '1000 Caracteres','rows':'4' }))
    epi = forms.CharField(label='EPI',required=False ,widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '1000 Caracteres','rows':'4'  }))
    epc = forms.CharField(label='EPC',required=False ,widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '1000 Caracteres', 'rows':'4' }))
    recomendacao = forms.CharField(label='Recomendação',required=False ,widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '1000 Caracteres', 'rows':'4' }))
    observacao = forms.CharField(label='Observação',required=False ,widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '1000 Caracteres', 'rows':'4' }))

    def save(self):
        _PopForm = super(PopForm, self).save(commit=False)
        _PopForm.save()
        return _PopForm

class TarefaForm(ModelForm):
    class Meta:
        model = Tarefa
        fields = ['codigo_pop','codigo', 'descricao']

    codigo_pop = forms.CharField(label='POP', widget=forms.TextInput(attrs={'readonly':'readonly','class': 'form-control', 'placeholder': '0000' }))
    codigo = forms.CharField(label='Código' ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0' }))
    descricao = forms.CharField(label='Descrição' ,widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '500 Caracteres', 'rows':'4' }))

    def save(self):
        _TarefaForm = super(TarefaForm, self).save(commit=False)
        _TarefaForm.save()
        return _TarefaForm

class ProcedimentoForm(ModelForm):
    class Meta:
        model = Procedimento
        fields = ['codigo','descricao','observacao','codigo_tarefa']

    codigo_tarefa = forms.CharField(label='',widget=forms.HiddenInput())
    codigo = forms.CharField(label='Código' ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0'}))
    descricao = forms.CharField(label='Descrição',widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '1000 Caracteres', 'rows':'4' }))
    observacao = forms.CharField(label='Observação',required=False ,widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '1000 Caracteres', 'rows':'4' }))
        

    def save(self):
        _ProcedimentoForm = super(ProcedimentoForm, self).save(commit=False)
        _ProcedimentoForm.save()
        return _ProcedimentoForm

class FolhaObservacaoForm(ModelForm):
    class Meta:
        model = FolhaObservacao
        fields = ['folha','cod_processo','nome_peca','nome_maquina','nome_matricula_operador',
                  'experiencia_servico','mestre','data','numero_operacao','numero_peca',
                  'numero_maquina','sexo','material','numero_secao','inicio','fim','numero_maquinas']

    lista_s = []
    lista_s.append(('masculino', 'Masculino'))
    lista_s.append(('feminino', 'Feminino'))

    processo_list = Processo.objects.all()
    lista_p = []
    for obj in processo_list:
        lista_p.append((obj.codigo, obj.descricao))

    folha = forms.CharField(label='Folha' ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '5 Caracteres'}))
    cod_processo = forms.CharField(label='Processo', widget=forms.Select(choices=lista_p,attrs={'class': 'form-control form-control-sm','data-toggle': 'dropdown'}))
    nome_peca = forms.CharField(label='Nome da Peça' ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '100 Caracteres'}))
    nome_maquina = forms.CharField(label='Nome da Máquina' ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '100 Caracteres'}))
    nome_matricula_operador = forms.CharField(label='Nome - Matrícula do Operador' ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '100 Caracteres'}))
    experiencia_servico = forms.CharField(label='Experiência do Serviço' ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '100 Caracteres'}))
    mestre = forms.CharField(label='Mestre' ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '100 Caracteres'}))
    data = forms.DateField(label='Data',initial=datetime.datetime.now(),widget=DateInput(attrs={'class': 'form-control'}))
    numero_operacao = forms.CharField(label='N. Operação' ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0'}))
    numero_peca = forms.CharField(label='N. da Peça' ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0'}))
    numero_maquina = forms.CharField(label='N. da Máquina' ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0'}))
    sexo = forms.CharField(label='Sexo', widget=forms.Select(choices=lista_s,attrs={'class': 'form-control form-control-sm','data-toggle': 'dropdown'}))
    material = forms.CharField(label='Material' ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '100 Caracteres'}))
    numero_secao = forms.CharField(label='N. Seção' ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '25 Caracteres'}))
    inicio = forms.CharField(label='Inicio' ,required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00:00:00'}))
    fim = forms.CharField(label='Fim' ,required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00:00:00'}))
    numero_maquinas = forms.CharField(label='N. Máquinas',required=False ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0'}))

class FolhaElementoForm(ModelForm):
    class Meta:
        model = FolhaElemento
        fields = ['id_folha','elemento','velocidade','avanco']

    id_folha = forms.CharField(label='',widget=forms.HiddenInput())
    ordinal = forms.IntegerField(label='Ordinal',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0'}))
    elemento = forms.CharField(label='Elemento' ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '100 Caracteres'}))
    velocidade = forms.CharField(label='Velocidade' ,required=False ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10 Caracteres'}))
    avanco = forms.CharField(label='Avanço' ,required=False ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10 Caracteres'}))

    t1 = forms.FloatField(label='Tempo 1',required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'value': '0.00'}))
    t2 = forms.FloatField(label='Tempo 2',required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'value': '0.00'}))
    t3 = forms.FloatField(label='Tempo 3',required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'value': '0.00'}))
    t4 = forms.FloatField(label='Tempo 4',required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'value': '0.00'}))
    t5 = forms.FloatField(label='Tempo 5',required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'value': '0.00'}))
    t6 = forms.FloatField(label='Tempo 6',required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'value': '0.00'}))
    t7 = forms.FloatField(label='Tempo 7',required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'value': '0.00'}))
    t8 = forms.FloatField(label='Tempo 8',required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'value': '0.00'}))
    t9 = forms.FloatField(label='Tempo 9',required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'value': '0.00'}))
    t10 = forms.FloatField(label='Tempo 10',required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'value': '0.00'}))

    def save(self,ordinal,id_folha,elemento,velocidade,avanco,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10):
        _FolhaElementoForm = super(FolhaElementoForm, self).save(commit=False)
        objElemento = FolhaElemento()
        objElemento.id_folha=id_folha
        objElemento.ordinal = ordinal
        objElemento.elemento=elemento
        objElemento.velocidade=velocidade
        objElemento.avanco=avanco
        objElemento.save()

        objTempo1 = salvarTempo(objElemento.id,1,t1)
        objTempo1.save()
        objTempo2 = salvarTempo(objElemento.id,2,t2)
        objTempo2.save()
        objTempo3 = salvarTempo(objElemento.id,3,t3)
        objTempo3.save()
        objTempo4 = salvarTempo(objElemento.id,4,t4)
        objTempo4.save()
        objTempo5 = salvarTempo(objElemento.id,5,t5)
        objTempo5.save()
        objTempo6 = salvarTempo(objElemento.id,6,t6)
        objTempo6.save()
        objTempo7 = salvarTempo(objElemento.id,7,t7)
        objTempo7.save()
        objTempo8 = salvarTempo(objElemento.id,8,t8)
        objTempo8.save()
        objTempo9 = salvarTempo(objElemento.id,9,t9)
        objTempo9.save()
        objTempo10 = salvarTempo(objElemento.id,10,t10)
        objTempo10.save()

        return _FolhaElementoForm

class ElementoTempoForm(ModelForm):
    class Meta:
        model = ElementoTempo
        fields = ['id_elemento','sequencial','tempo']

    id_elemento = forms.CharField(label='',widget=forms.HiddenInput())
    sequencial = forms.CharField(label='Sequencia' ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0'}))
    tempo = forms.CharField(label='Tempo' ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0.0'}))