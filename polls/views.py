import datetime, calendar,os

from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import *
from .models import *

# funções
def meses():
    meses_list = []
    meses_list.append(datetime.datetime(2019, 1, 1))
    meses_list.append(datetime.datetime(2019, 2, 1))
    meses_list.append(datetime.datetime(2019, 3, 1))
    meses_list.append(datetime.datetime(2019, 4, 1))
    meses_list.append(datetime.datetime(2019, 5, 1))
    meses_list.append(datetime.datetime(2019, 6, 1))
    meses_list.append(datetime.datetime(2019, 7, 1))
    meses_list.append(datetime.datetime(2019, 8, 1))
    meses_list.append(datetime.datetime(2019, 9, 1))
    meses_list.append(datetime.datetime(2019, 10, 1))
    meses_list.append(datetime.datetime(2019, 11, 1))
    meses_list.append(datetime.datetime(2019, 12, 1))
    return meses_list

# Create your views here.
def telalogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                #context = {'erro': 'Usuário logado!'}
                return HttpResponseRedirect(reverse('index'))
                #return render(request, 'polls/index.html')
            else:
                context = {'erro': 'Conta desabilitada'}
                return render(request, 'polls/login.html',context)
        else:
            context = {'erro': 'Usuário ou Senha inválido!'}
            return render(request, 'polls/login.html', context)
    else:
        return render(request, 'polls/login.html')

def sair(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def index(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('login'))
    #user.is_superuser
    else:
        empresa_list = Empresa.objects.order_by('nome')[:5]
        setor_list = Setor.objects.order_by('nome')
        faturamento_atual_list = Faturamento.objects.filter(data__year=datetime.datetime.now().year,
                                                        data__month=datetime.datetime.now().month)
        devolucao_atual_valor_list = Devolucao.objects.raw(
            'SELECT idempresa, \'\'||(cast(SUM(VALOR) as int)) AS valor, id FROM polls_devolucao '
            'WHERE strftime(\'%Y\',data_devolucao)=Strftime(\'%Y\',DATE(\'NOW\')) '
            'AND strftime(\'%m\',data_devolucao)=strftime(\'%m\',DATE(\'NOW\')) '
            'GROUP BY IDEMPRESA',
            translations={'idempresa': 'idempresa', 'valor': 'valor', 'id': 'id'})

        ultimo_dia = calendar.monthlen(2020, 8) + 1
        dias_mes_list = []
        for i in range(1, ultimo_dia):
            dias_mes_list.append(i)

        faturamento_graf_mes_list = []
        for dia in dias_mes_list:
            dd = str(dia)
            dados = []
            dados.append(dd)
            for empresa in empresa_list:
                temp = 0
                for fat in faturamento_atual_list:
                    if fat.idempresa == empresa.idempresa and dia == int(fat.data.strftime("%d")):
                        temp = str(fat.faturamento)
                dados.append(temp)
            if len(dados) == 1 :
                faturamento_graf_mes_list.append("x: " + dados[0] + ", y: 0, z: 0, w: 0")
            elif len(dados) == 2 :
                faturamento_graf_mes_list.append("x: " + dados[0] + ", y: " + str(dados[1]) + ", z: 0, w: 0")
            elif len(dados) == 3:
                faturamento_graf_mes_list.append("x: " + dados[0] + ", y: " + str(dados[1]) + ", z: " + str(dados[2]) + ", w: 0")
            elif len(dados) == 4 :
                faturamento_graf_mes_list.append("x: " + dados[0] + ", y: " + str(dados[1]) + ", z: " + str(dados[2]) + ", w: " + str(dados[3]))

        carteira_atual_list = Carteira.objects.raw('SELECT '
                                           'e.nome as apelido,e.idempresa,'
                                           '\'\'||(select f.carteira from polls_carteira as f where f.idempresa=e.idempresa and strftime(\'%Y%m\',f.data)=strftime(\'%Y%m\',date(\'now\')) order by data desc limit 1) as valor,'
                                           'e.id '
                                           'from polls_empresa as e order by 1',
                                           translations={'apelido': 'apelido', 'valor': 'valor', 'id': 'id',
                                                         'idempresa': 'idempresa'})

        reprogramacao_grafico_list = Reprogramacao.objects.raw('SELECT e.id,'
                                                       'e.idempresa '
                                                       ',e.apelido as nome, e.nome as indice'
                                                       ', \'\'||Cast(coalesce(( '
                                                       'SELECT '
                                                       'sum(r.custo) from polls_reprogramacao as r '
                                                       'where strftime(\'%Y\',r.data)=strftime(\'%Y\',DATE(\'NOW\')) '
                                                       'and strftime(\'%m\',r.data)=strftime(\'%m\',DATE(\'NOW\')) '
                                                       'and r.idempresa=e.idempresa '
                                                       'and r.retrabalho=0 '
                                                       ' ),0)as integer ) as reprogramacao '
                                                       ',\'\'||Cast(coalesce(( '
                                                       'SELECT '
                                                       'sum(r.custo) from polls_reprogramacao as r '
                                                       'where strftime(\'%Y\',r.data)=strftime(\'%Y\',DATE(\'NOW\')) '
                                                       'and strftime(\'%m\',r.data)=strftime(\'%m\',DATE(\'NOW\')) '
                                                       'and r.idempresa=e.idempresa '
                                                       'and r.retrabalho=1 '
                                                       '),0) as integer ) as retrabalho '
                                                       ',coalesce((select '
                                                       'sum(f.faturamento) from polls_faturamento as f '
                                                       'where f.idempresa=e.idempresa '
                                                       'and strftime(\'%Y\',f.data) = strftime(\'%Y\',DATE(\'NOW\'))  '
                                                       'and strftime(\'%m\',f.data) = strftime(\'%m\',DATE(\'NOW\'))),0) as faturamento '
                                                       'FROM polls_empresa as e '
                                                       'ORDER by 4',
                                                       translations={'id': 'id',
                                                                     'idempresa': 'idempresa',
                                                                     'nome': 'nome',
                                                                     'reprogramacao': 'reprogramacao',
                                                                     'retrabalho': 'retrabalho',
                                                                     'faturamento': 'faturamento'})
        dados_rep = [];
        for obj in reprogramacao_grafico_list:
            dados_rep.append("{x: " + obj.nome + ", y: 1 " + ", z: 2 },")

        faturamento_total_list = Faturamento.objects.raw('select '
                                                 'idempresa,sum(faturamento ) as valor,id '
                                                 'from polls_faturamento '
                                                 'where  strftime(\'%Y\',data) = strftime(\'%Y\',DATE(\'NOW\'))  '
                                                 'and strftime(\'%m\',data) = strftime(\'%m\',DATE(\'NOW\')) '
                                                 'group by 1', translations={'id': 'id', 'idempresa': 'idempresa',
                                                                             'valor': 'valor'})


        class giroCarteira:
            idempresa = 0
            giro = 0


        list_giro = []
        for obj in faturamento_total_list:
            for obj1 in carteira_atual_list:
                if obj.idempresa == obj1.idempresa:
                    objg = giroCarteira()
                    objg.idempresa = obj.idempresa
                    if obj.valor>0 and obj1.valor != None :
                        objg.giro = (obj.valor / int(obj1.valor))
                    else:
                        objg.giro = 0
                    list_giro.append(objg)

        context = {'empresa_list': empresa_list,
           'setor_list': setor_list,
           'carteira_atual_list': carteira_atual_list,
           'faturamento_graf_mes_list': faturamento_graf_mes_list,
           'faturamento_total_list': faturamento_total_list,
           'devolucao_atual_valor_list': devolucao_atual_valor_list,
           'reprogramacao_grafico_list': reprogramacao_grafico_list,
           'list_giro': list_giro}
        return render(request, 'polls/index.html', context)

def carteira(request):
    empresa_list = Empresa.objects.order_by('nome')
    carteira_atual_list = Carteira.objects.filter(data__year=datetime.datetime.now().year,
                                                  data__month=datetime.datetime.now().month).order_by('data')

    carteira_atual_valor_list = Carteira.objects.raw('SELECT '
                                                     'e.nome as apelido,e.idempresa,'
                                                     '\'\'||(select f.carteira from polls_carteira as f where f.idempresa=e.idempresa and strftime(\'%Y%m\',f.data)=strftime(\'%Y%m\',date(\'now\')) order by data desc limit 1) as valor,'
                                                     'e.id '
                                                     'from polls_empresa as e order by 1',
                                                     translations={'idempresa': 'idempresa', 'apelido': 'apelido',
                                                                   'valor': 'valor', 'id': 'id'})

    carteira_anos_list = Carteira.objects.raw(
        'SELECT strftime(\'%Y\',data) as ano,id from polls_carteira group by 1 order by 1 desc',
        translations={'ano': 'ano', 'id': 'id'})
    carteira_dias_list = Carteira.objects.raw(
        'SELECT strftime(\'%d\',data) as ano,id from polls_carteira where  strftime(\'%Y%m\',data) = strftime(\'%Y%m\',DATE(\'NOW\')) group by 1 order by 1 ',
        translations={'dias': 'dias', 'id': 'id'})

    faturamento_total_list = Faturamento.objects.raw('select '
                                                     'idempresa,sum(faturamento ) as valor,id '
                                                     'from polls_faturamento '
                                                     'where  strftime(\'%Y\',data) = strftime(\'%Y\',DATE(\'NOW\'))  '
                                                     'and strftime(\'%m\',data) = strftime(\'%m\',DATE(\'NOW\')) '
                                                     'group by 1', translations={'id': 'id', 'idempresa': 'idempresa',
                                                                                 'valor': 'valor'})

    class giroCarteira:
        idempresa = 0
        giro = 0

    list_giro = []
    for obj in faturamento_total_list:
        for obj1 in carteira_atual_valor_list:
            if obj.idempresa == obj1.idempresa:
                objg = giroCarteira()
                objg.idempresa = obj.idempresa
                if obj.valor > 0 and obj1.valor != None:
                    objg.giro = (obj.valor / int(obj1.valor))
                else:
                    objg.giro = 0
                list_giro.append(objg)

    context = {'empresa_list': empresa_list,
               'carteira_atual_list': carteira_atual_list,
               'carteira_anos_list': carteira_anos_list,
               'carteira_dias_list': carteira_dias_list,
               'carteira_atual_valor_list': carteira_atual_valor_list,
               'meses_list': meses(),
               'list_giro': list_giro}
    return render(request, 'polls/carteira.html', context)

def devolucao(request):
    empresa_list = Empresa.objects.order_by('nome')[:5]

    devolucao_atual_list = Devolucao.objects.filter(data_devolucao__year=datetime.datetime.now().year,
                                                    data_devolucao__month=datetime.datetime.now().month).order_by(
        'data_devolucao')
    devolucao_atual_valor_list = Devolucao.objects.raw(
        'SELECT idempresa, \'\'||(cast(SUM(VALOR) as int)) AS valor, id FROM polls_devolucao '
        'WHERE strftime(\'%Y\',data_devolucao)=Strftime(\'%Y\',DATE(\'NOW\')) '
        'AND strftime(\'%m\',data_devolucao)=strftime(\'%m\',DATE(\'NOW\')) '
        'GROUP BY IDEMPRESA',
        translations={'idempresa': 'idempresa', 'valor': 'valor', 'id': 'id'})

    devolucao_anos_list = Devolucao.objects.raw(
        'SELECT strftime(\'%Y\',data_devolucao) as ano,id from polls_devolucao group by 1 order by 1 desc',
        translations={'ano': 'ano', 'id': 'id'})

    relatorio_list = Relatorio.objects.order_by('descricao')[:5]
    context = {'empresa_list': empresa_list,
               'relatorio_list': relatorio_list,
               'devolucao_atual_list': devolucao_atual_list,
               'devolucao_atual_valor_list': devolucao_atual_valor_list,
               'devolucao_anos_list': devolucao_anos_list,
               'meses': meses()}
    return render(request, 'polls/devolucao.html', context)

def faturamento(request):
    empresa_list = Empresa.objects.order_by('nome')
    faturamento_atual_list = Faturamento.objects.filter(data__year=datetime.datetime.now().year,
                                                        data__month=datetime.datetime.now().month)
    faturamento_anos_list = Carteira.objects.raw(
        'SELECT strftime(\'%Y\',data) as ano,id from polls_faturamento group by 1 order by 1 desc',
        translations={'ano': 'ano', 'id': 'id'})
    faturamento_atual_total_list = Carteira.objects.raw(
        'select idempresa,sum(faturamento) as valor, id from polls_faturamento '
        'WHERE strftime(\'%Y%m\',data)=Strftime(\'%Y%m\',DATE(\'NOW\')) '
        ' group by 1',
        translations={'id': 'id', 'idempresa': 'idempresa', 'valor': 'valor'})
    ultimo_dia = calendar.monthlen(datetime.datetime.now().year, datetime.datetime.now().month) + 1
    dias_mes_list = []
    for i in range(1, ultimo_dia):
        dias_mes_list.append(i)

    faturamento_graf_mes_list = []
    for dia in dias_mes_list:
        dd = str(dia)
        dados = []
        dados.append(dd)
        for empresa in empresa_list:
            temp = 0
            for fat in faturamento_atual_list:
                if fat.idempresa == empresa.idempresa and dia == int(fat.data.strftime("%d")):
                    temp = str(fat.faturamento)
            dados.append(temp)

        if len(dados) == 1:
            faturamento_graf_mes_list.append("x: " + dados[0] + ", y: 0, z: 0, w: 0")
        elif len(dados) == 2:
            faturamento_graf_mes_list.append("x: " + dados[0] + ", y: " + str(dados[1]) + ", z: 0, w: 0")
        elif len(dados) == 3:
            faturamento_graf_mes_list.append(
                "x: " + dados[0] + ", y: " + str(dados[1]) + ", z: " + str(dados[2]) + ", w: 0")
        elif len(dados) == 4:
            faturamento_graf_mes_list.append(
                "x: " + dados[0] + ", y: " + str(dados[1]) + ", z: " + str(dados[2]) + ", w: " + str(dados[3]))

    context = {'empresa_list': empresa_list,
               'faturamento_atual_list': faturamento_atual_list,
               'anos_list': faturamento_anos_list,
               'meses_list': meses,
               'faturamento_atual_total_list': faturamento_atual_total_list,
               'dias_mes_list': dias_mes_list,
               'faturamento_graf_mes_list': faturamento_graf_mes_list}
    return render(request, 'polls/faturamento.html', context)

def prazoentrega(request):
    empresa_list = Empresa.objects.order_by('nome')[:5]
    linhas_producao_list = LinhaProducao.objects.order_by('descricao')
    prazo_anos_list = Carteira.objects.raw(
        'SELECT strftime(\'%Y\',data) as ano,id from polls_prazoentrega group by 1 order by 1 DESC',
        translations={'id': 'id', 'ano': 'ano'})[:2];

    prazo_atual_list = PrazoEntrega.objects.raw('SELECT '
                                                'strftime(\'%Y\',p.data)||\'-\'||strftime(\'%m\',p.data)||\'-01\' as data, '
                                                'l.descricao, '
                                                'avg(p.prazo) as prazo, p.id as id '
                                                'from polls_prazoentrega as p '
                                                'inner join polls_linhaproducao l on l.codigo1=p.linhaproducao '
                                                'where strftime(\'%Y\',p.data)=strftime(\'%Y\',DATE(\'NOW\')) AND strftime(\'%m\',p.data)=strftime(\'%m\',DATE(\'NOW\')) '
                                                'group by 1,2 '
                                                'order by 2 ',
                                                translations={'id': 'id', 'data': 'data', 'descricao': 'descricao',
                                                              'prazo': 'prazo'})

    context = {'empresa_list': empresa_list,
               'prazo_atual_list': prazo_atual_list,
               'anos_list': prazo_anos_list,
               'linhas_producao_list': linhas_producao_list,
               'meses_list': meses}
    return render(request, 'polls/prazoentrega.html', context)

def producaogeral(request):
    setor_list = Setor.objects.order_by('nome')
    ultimo_dia = calendar.monthlen(2020, 8) + 1
    dias_mes_list = []
    for i in range(1, ultimo_dia):
        dias_mes_list.append(i)

    producao_atual_list = ProducaoSetor.objects.raw(
        'SELECT p.id, cast(strftime(\'%d\', p.data) as integer) as dia, s.codigo, s.nome, '
        'cast(sum(p.quantidade) as integer) as quantidade FROM polls_producaosetor as p '
        'inner join polls_setor s on trim(s.codigo) = trim(p.cod_setor) '
        'WHERE strftime(\'%Y\', p.data) = strftime(\'%Y\',DATE(\'NOW\')) and strftime(\'%m\', p.data) = strftime(\'%m\',DATE(\'NOW\')) '
        'group by 2, 3, 4 order by 2, 4 ',
        translations={'id': 'id', 'dia': 'dia', 'codigo': 'codigo', 'nome': 'nome', 'quantidade': 'quantidade'})

    producao_anos_list = ProducaoSetor.objects.raw(
        'SELECT p.id, strftime(\'%Y\',p.data) as ano FROM polls_producaosetor as p group by 2 order by 2 desc',
        translations={'id': 'id', 'ano': 'ano'})

    producao_valores_anos_list = ProducaoSetor.objects.raw(
        'SELECT p.id,strftime(\'%Y\',p.data) as ano, strftime(\'%m\',p.data) as mes, '
        'p.cod_setor as codigo,s.nome,sum(p.quantidade) as quantidade '
        'FROM polls_producaosetor as p '
        'inner join polls_setor s on trim(s.codigo)=trim(p.cod_setor) '
        'group by 2,3,4,5 order by 2,3,5',
        translations={'id': 'id', 'ano': 'ano', 'mes': 'mes', 'codigo': 'codigo',
                      'nome': 'nome', 'quantidade': 'quantidade'})
    producao_atual_grafica = ProducaoSetor.objects.raw(
        'SELECT p.id,s.nome,\'\'||(cast(SUM(p.quantidade) as int)) as quantidade '
        'FROM polls_producaosetor as p '
        'inner join polls_setor s on trim(s.codigo)=trim(p.cod_setor) '
        'WHERE strftime(\'%Y\',p.data)=strftime(\'%Y\',DATE(\'NOW\')) '
        'and strftime(\'%m\',p.data)=strftime(\'%m\',DATE(\'NOW\')) '
        'group by 2 order by 2',
        translations={'id': 'id', 'nome': 'nome', 'quantidade': 'quantidade'})
    producao_atual_total = ProducaoSetor.objects.raw(
        'SELECT p.id,\'\'||coalesce(cast(sum(p.quantidade)as int),0) as quantidade FROM polls_producaosetor as p '
        'inner join polls_setor s on trim(s.codigo)=trim(p.cod_setor) '
        'WHERE strftime(\'%Y\',p.data)=strftime(\'%Y\',DATE(\'NOW\')) '
        'and strftime(\'%m\',p.data)=strftime(\'%m\',DATE(\'NOW\'))',
        translations={'id': 'id', 'quantidade': 'quantidade'})

    total_mes = ''
    for objeto in producao_atual_total:
        total_mes = objeto.quantidade

    context = {
        'setor_list': setor_list,
        'dias_mes_list': dias_mes_list,
        'producao_atual_list': producao_atual_list,
        'anos_list': producao_anos_list,
        'producao_valores_anos_list': producao_valores_anos_list,
        'meses_list': meses,
        'producao_atual_grafica': producao_atual_grafica,
        'total_mes': total_mes}
    return render(request, 'polls/producaogeral.html', context)

def reprogramacaoretrabalho(request):
    empresa_list = Empresa.objects.order_by('nome')
    setor_list = Setor.objects.order_by('nome')
    relatorio_list = Relatorio.objects.order_by('descricao')

    reprogramacao_atual_list = Reprogramacao.objects.raw('SELECT '
                                                         't.*,round((custo*100/(select sum(f.faturamento) from polls_faturamento as f where f.idempresa=t.idempresa and t.ano = strftime(\'%Y\',f.data)  and strftime(\'%m\',DATE(\'NOW\')) = strftime(\'%m\',f.data))),1) as indice '
                                                         'FROM (SELECT r.id,'
                                                         'strftime(\'%Y\',r.data) as ano,'
                                                         'strftime(\'%d\',r.data) as dia,'
                                                         'r.idempresa,'
                                                         'case when r.retrabalho=1 then \'Retrabalho\' else \'Reprogramacao\' end as tipo,'
                                                         'SUM(r.quantidade) as quantidade,'
                                                         'round(SUM(r.custo),2) AS custo '
                                                         'FROM polls_reprogramacao as r '
                                                         'WHERE strftime(\'%Y\',r.data)=strftime(\'%Y\',DATE(\'NOW\')) '
                                                         'and strftime(\'%m\',r.data)=strftime(\'%m\',DATE(\'NOW\')) GROUP BY 2,3,4,5) as T',
                                                         translations={'id': 'id',
                                                                       'ano': 'ano',
                                                                       'dia': 'dia',
                                                                       'idempresa': 'idempresa',
                                                                       'tipo': 'tipo',
                                                                       'quantidade': 'quantidade',
                                                                       'custo': 'custo',
                                                                       'indice': 'indice'})

    reprogramacao_historico_list = Reprogramacao.objects.raw('SELECT '
                                                             't.*,round((custo*100/(select sum(f.faturamento) from polls_faturamento as f where f.idempresa=t.idempresa and t.ano = strftime(\'%Y\',f.data)  and t.mes = strftime(\'%m\',f.data))),2) as indice '
                                                             'FROM (SELECT r.id,'
                                                             'strftime(\'%Y\',r.data) as ano,'
                                                             'strftime(\'%m\',r.data) as mes,'
                                                             'r.idempresa,'
                                                             'case when r.retrabalho=1 then \'Retrabalho\' else \'Reprogramacao\' end as tipo,'
                                                             'cast(SUM(r.quantidade) as integer) as quantidade,'
                                                             'round(SUM(r.custo),2) AS custo '
                                                             'FROM polls_reprogramacao as r '
                                                             'GROUP BY 2,3,4,5 order by 2,3) as T ',
                                                             translations={'id': 'id',
                                                                           'ano': 'ano',
                                                                           'mes': 'mes',
                                                                           'idempresa': 'idempresa',
                                                                           'tipo': 'tipo',
                                                                           'quantidade': 'quantidade',
                                                                           'custo': 'custo',
                                                                           'indice': 'indice'})

    reprogramacao_grafico_list = Reprogramacao.objects.raw('SELECT e.id,'
                                                           'e.idempresa '
                                                           ',e.apelido as nome, e.nome as indice'
                                                           ', \'\'||Cast(coalesce(( '
                                                           'SELECT '
                                                           'sum(r.custo) from polls_reprogramacao as r '
                                                           'where strftime(\'%Y\',r.data)=strftime(\'%Y\',DATE(\'NOW\')) '
                                                           'and strftime(\'%m\',r.data)=strftime(\'%m\',DATE(\'NOW\')) '
                                                           'and r.idempresa=e.idempresa '
                                                           'and r.retrabalho=0 '
                                                           ' ),0)as integer ) as reprogramacao '
                                                           ',\'\'||Cast(coalesce(( '
                                                           'SELECT '
                                                           'sum(r.custo) from polls_reprogramacao as r '
                                                           'where strftime(\'%Y\',r.data)=strftime(\'%Y\',DATE(\'NOW\')) '
                                                           'and strftime(\'%m\',r.data)=strftime(\'%m\',DATE(\'NOW\')) '
                                                           'and r.idempresa=e.idempresa '
                                                           'and r.retrabalho=1 '
                                                           '),0) as integer ) as retrabalho '
                                                           ',coalesce((select '
                                                           'sum(f.faturamento) from polls_faturamento as f '
                                                           'where f.idempresa=e.idempresa '
                                                           'and strftime(\'%Y\',f.data) = strftime(\'%Y\',DATE(\'NOW\'))  '
                                                           'and strftime(\'%m\',f.data) = strftime(\'%m\',DATE(\'NOW\'))),0) as faturamento '
                                                           'FROM polls_empresa as e '
                                                           'ORDER by 4',
                                                           translations={'id': 'id',
                                                                         'idempresa': 'idempresa',
                                                                         'nome': 'nome',
                                                                         'reprogramacao': 'reprogramacao',
                                                                         'retrabalho': 'retrabalho',
                                                                         'faturamento': 'faturamento'})

    reprogramacao_anos_list = Carteira.objects.raw(
        'SELECT strftime(\'%Y\',data) as ano,id from polls_reprogramacao group by 1 order by 1 DESC',
        translations={'id': 'id', 'ano': 'ano'});

    context = {'empresa_list': empresa_list,
               'setor_list': setor_list,
               'relatorio_list': relatorio_list,
               'reprogramacao_atual_list': reprogramacao_atual_list,
               'anos_list': reprogramacao_anos_list,
               'meses_list': meses,
               'reprogramacao_historico_list': reprogramacao_historico_list,
               'reprogramacao_grafico_list': reprogramacao_grafico_list}
    return render(request, 'polls/reprogramacaoretrabalho.html', context)

def erro(request, menssagem):
    context = {'menssagem': menssagem}
    return render(request, 'polls/erro.html', context)

def globalmanut(request, id,idsec):
    empresa_list = Empresa.objects.all()
    linhaproducao_list = LinhaProducao.objects.all().order_by('descricao')
    setor_list = Setor.objects.all().order_by('nome')
    setor = Setor
    empresa = Empresa
    if id != '4' and id != '5' and  id != '6':
        empresa = Empresa.objects.get(idempresa=idsec)
    dados_list = []
    titulo = ''
    titulo2 = ''
    class Dado:
        id = int
        idsec = str
        data = datetime
        valor = float
    if id == '1':
        titulo = 'Alterar Dados Carteira'
        titulo2 = empresa.nome
        obj_list = Carteira.objects.filter(idempresa=idsec).order_by('-data')
        for obj in obj_list:
            dado = Dado()
            dado.id = obj.id
            dado.data = obj.data
            dado.valor = obj.carteira
            dado.idsec = idsec
            dados_list.append(dado)
    elif id == '2':
        titulo = 'Alterar Dados Devolução'
        titulo2 = empresa.nome
        obj_list = Devolucao.objects.filter(idempresa=idsec).order_by('-data_devolucao')
        for obj in obj_list:
            dado = Dado()
            dado.id = obj.id
            dado.data = obj.data_devolucao
            dado.valor = obj.valor
            dado.idsec = idsec
            dados_list.append(dado)
    elif id == '3':
        titulo = 'Alterar Faturamento'
        titulo2 = empresa.nome
        obj_list = Faturamento.objects.filter(idempresa=idsec).order_by('-data')
        for obj in obj_list:
            dado = Dado()
            dado.id = obj.id
            dado.data = obj.data
            dado.valor = obj.faturamento
            dado.idsec = idsec
            dados_list.append(dado)
    elif id == '4':
        linhaproducao = LinhaProducao.objects.get(codigo1=idsec)
        titulo = 'Alterar Prazo Entrega'
        titulo2 = linhaproducao.descricao
        obj_list = PrazoEntrega.objects.filter(linhaproducao=idsec).order_by('-data')
        for obj in obj_list:
            dado = Dado()
            dado.id = obj.id
            dado.data = obj.data
            dado.valor = obj.prazo
            dado.idsec = idsec
            dados_list.append(dado)
    elif id == '5':
        setor = Setor.objects.get(codigo=idsec)
        titulo = 'Alterar Reprogramação & Retrabalho'
        titulo2 = setor.nome
        obj_list = Reprogramacao.objects.filter(idsetor=idsec).order_by('-data')
        for obj in obj_list:
            dado = Dado()
            dado.id = obj.id
            dado.data = obj.data
            dado.valor = obj.custo
            dado.idsec = idsec
            dados_list.append(dado)
    elif id == '6':
        setor = Setor.objects.get(codigo=idsec)
        titulo = 'Alterar Produção Setor'
        titulo2 = setor.nome
        obj_list = ProducaoSetor.objects.filter(cod_setor=idsec).order_by('-data')[:100]
        for obj in obj_list:
            dado = Dado()
            dado.id = obj.id
            dado.data = obj.data
            dado.valor = obj.quantidade
            dado.idsec = idsec
            dados_list.append(dado)

    context = {'titulo': titulo,
               'titulo2': titulo2,
                'empresa_list':empresa_list,
               'linhaproducao_list': linhaproducao_list,
               'setor_list': setor_list,
               'empresa':empresa,
               'tipo': id,
               'setor':setor,
               'dados_list': dados_list}

    return render(request, 'polls/globalmanut.html', context)

def setor(request, id):
    setor = Setor.objects.get(codigo=id)
    subsetor_list = SubSetor.objects.filter(idsetor=id).order_by('nome')
    pop_list = POP.objects.filter(codsetor=id).order_by('tarefa')
    ultimo_dia = calendar.monthlen(2020, 8) + 1
    dias_mes_list = []
    for i in range(1, ultimo_dia):
        dias_mes_list.append(i)

    setor_anos_list = ProducaoSetor.objects.raw(
        'SELECT strftime(\'%Y\',data) as ano,id from polls_producaosetor where cod_setor=\''+id+'\' group by 1 order by 1 desc',
        translations={'ano': 'ano', 'id': 'id'})
    pontoscontrole_list = Ponto_Controle.objects.filter(idsetor=id).order_by('descricao')

    producao_atual_list = ProducaoSetor.objects.raw('SELECT '
                                                    'CAST(strftime(\'%d\',p.data) AS INT) as dia,'
                                                    'cast(sum(quantidade) as int) as quantidade, p.id '
                                                    'FROM polls_producaosetor as p '
                                                    'where strftime(\'%Y\',p.data)=strftime(\'%Y\',DATE(\'NOW\')) '
                                                    'and strftime(\'%m\',p.data)=strftime(\'%m\',DATE(\'NOW\')) '
                                                    'and p.cod_setor=\'' + id + '\''
                                                                                'group by 1 '
                                                                                'order by 1', translations={'id': 'id',
                                                                                                            'dia': 'dia',
                                                                                                            'quantidade': 'quantidade'})

    reprogramacao_atual_list = Reprogramacao.objects.raw('SELECT '
                                                         'CAST(strftime(\'%d\',p.data) AS INT) as dia,'
                                                         'sum(quantidade) as quantidade, p.id '
                                                         'FROM polls_reprogramacao as p '
                                                         'where strftime(\'%Y\',p.data)=strftime(\'%Y\',DATE(\'NOW\')) '
                                                         'and strftime(\'%m\',p.data)=strftime(\'%m\',DATE(\'NOW\')) '
                                                         'and p.idsetor=\'' + id + '\' and p.retrabalho=0 '
                                                                                   'group by 1 '
                                                                                   'order by 1',
                                                         translations={'id': 'id',
                                                                       'dia': 'dia',
                                                                       'quantidade': 'quantidade'})

    retrabalho_atual_list = Reprogramacao.objects.raw('SELECT '
                                                      'CAST(strftime(\'%d\',p.data) AS INT) as dia,'
                                                      'cast(sum(quantidade) as int) as quantidade, p.id '
                                                      'FROM polls_reprogramacao as p '
                                                      'where strftime(\'%Y\',p.data)=strftime(\'%Y\',DATE(\'NOW\')) '
                                                      'and strftime(\'%m\',p.data)=strftime(\'%m\',DATE(\'NOW\')) '
                                                      'and p.idsetor=\'' + id + '\' and p.retrabalho=1 '
                                                                                'group by 1 '
                                                                                'order by 1', translations={'id': 'id',
                                                                                                            'dia': 'dia',
                                                                                                            'quantidade': 'quantidade'})

    retrabalho_list = Reprogramacao.objects.raw('SELECT '
                                                'm.descricao, '
                                                '\'\'||cast(sum(r.quantidade) as int) as quantidade, '
                                                'sum(r.custo) as custo, '
                                                'r.id '
                                                'FROM polls_reprogramacao as r '
                                                'INNER JOIN polls_motivo_reprogramacao m on m.idmotivo=r.idmotivo '
                                                'WHERE strftime(\'%Y-%m\',r.data)=strftime(\'%Y-%m\',DATE(\'NOW\')) '
                                                'and r.idsetor=\'' + id + '\' '
                                                                          'and retrabalho = 1  '
                                                                          'group by 1 order by 3 desc'
                                                , translations={'id': 'id',
                                                                'ddescricao': 'descricao',
                                                                'quantidade': 'quantidade',
                                                                'custo': 'custo'})

    reprogramacao_list = Reprogramacao.objects.raw('SELECT '
                                                   'm.descricao,'
                                                   '\'\'||Cast(sum(r.quantidade) as int) as quantidade,'
                                                   'sum(r.custo) as custo,'
                                                   'r.id '
                                                   'FROM polls_reprogramacao as r '
                                                   'INNER JOIN polls_motivo_reprogramacao m on m.idmotivo=r.idmotivo '
                                                   'WHERE strftime(\'%Y-%m\',r.data)=strftime(\'%Y-%m\',DATE(\'NOW\')) '
                                                   'and r.idsetor=\'' + id + '\' '
                                                                             'and retrabalho = 0  '
                                                                             'group by 1 order by 3 desc '
                                                   , translations={'id': 'id',
                                                                   'ddescricao': 'descricao',
                                                                   'quantidade': 'quantidade',
                                                                   'custo': 'custo'})
    setor_historico_list = ProducaoSetor.objects.raw('SELECT '
                                                     'strftime(\'%Y\',p.data) as ano,'
                                                     'strftime(\'%m\',p.data) as mes, '
                                                     'sum(p.quantidade) as quantidade,p.id, '
                                                     '(select sum(quantidade) from polls_reprogramacao as r where strftime(\'%Y%m\',r.data)=strftime(\'%Y%m\',p.data) and r.idsetor=p.cod_setor and r.retrabalho=0) as reprogramacao,'
                                                     '(select sum(quantidade) from polls_reprogramacao as r where strftime(\'%Y%m\',r.data)=strftime(\'%Y%m\',p.data) and r.idsetor=p.cod_setor and r.retrabalho=1) as retrabalho '
                                                     'FROM polls_producaosetor as p '
                                                     'where p.cod_setor=\'' + id + '\' group by 1,2 order by 1,2',
                                                     translations={'id': 'id',
                                                                   'ano': 'ano',
                                                                   'mes': 'mes',
                                                                   'quantidade': 'quantidade',
                                                                   'reprogramacao': 'reprogramacao',
                                                                   'retrabalho': 'retrabalho',
                                                                   'data': 'data'}
                                                     )


    for obj in setor_historico_list:
        obj.data = datetime.date(int(obj.ano), int(obj.mes), 1)

    pecas_reprogramadas = 0;
    custo_total_rep = 0;
    for obj in reprogramacao_list:
        pecas_reprogramadas += int(obj.quantidade)
        custo_total_rep += obj.custo

    pecas_retrabalhadas = 0;
    custo_total_ret = 0;
    for obj in retrabalho_list:
        pecas_retrabalhadas += int(obj.quantidade)
        custo_total_ret += obj.custo

    situaca_graf_list = []

    class objvalorgraf():
        dia = '0'
        prod = 0
        rep = 0
        ret = 0

    pecas_produzidas = 0;
    for dia in dias_mes_list:
        prod = 0
        rep = 0
        ret = 0

        for pr in producao_atual_list:
            if pr.dia == dia:
                prod = pr.quantidade

        for rp in reprogramacao_atual_list:
            if rp.dia == dia:
                rep = rp.quantidade

        for rt in retrabalho_atual_list:
            if rt.dia == dia:
                ret = rt.quantidade

        if prod > 0 or rep > 0 or ret > 0:
            valores = objvalorgraf()
            valores.dia = dia
            valores.prod = str(prod).replace(',', '')
            valores.rep = str(rep).replace(',', '')
            valores.ret = str(ret).replace(',', '')
            situaca_graf_list.append(
                "x: " + str(dia) + ", y: " + str(prod).replace(',', '') + ", z: " + str(ret).replace(',',
                                                                                                     '') + ", w: " + str(
                    rep).replace(',', ''))

        pecas_produzidas += prod

    context = {'setor': setor,
               'subsetor_list': subsetor_list,
               'dias': dias_mes_list,
               'producao_atual_list': producao_atual_list,
               'reprogramacao_atual_list': reprogramacao_atual_list,
               'retrabalho_atual_list': retrabalho_atual_list,
               'situaca_graf_list': situaca_graf_list,
               'reprogramacao_list': reprogramacao_list,
               'retrabalho_list': retrabalho_list,
               'pecas_reprogramadas': pecas_reprogramadas,
               'pecas_retrabalhadas': pecas_retrabalhadas,
               'pecas_produzidas': pecas_produzidas,
               'custo_total_rep': custo_total_rep,
               'custo_total_ret': custo_total_ret,
               'anos_list': setor_anos_list,
               'setor_historico_list': setor_historico_list,
               'cod_setor': id,
               'meses_list': meses(),
               'pontoscontrole_list': pontoscontrole_list,
               'pop_list': pop_list
               }

    return render(request, 'polls/setor.html', context)

def setor_layout(request, codigo):
    setor = Setor.objects.get(codigo=codigo)
    subsetor_list = SubSetor.objects.filter(idsetor=codigo).order_by('nome')
    pop_list = POP.objects.filter(codsetor=codigo).order_by('tarefa')
    setor_anos_list = ProducaoSetor.objects.raw(
        'SELECT strftime(\'%Y\',data) as ano,id from polls_producaosetor where cod_setor=\'' + codigo + '\' group by 1 order by 1 desc',
        translations={'ano': 'ano', 'id': 'id'})
    pontoscontrole_list = Ponto_Controle.objects.filter(idsetor=codigo).order_by('descricao')

    context = {'setor': setor,
               'subsetor_list': subsetor_list,
               'anos_list': setor_anos_list,
               'meses_list': meses(),
               'pontoscontrole_list': pontoscontrole_list,
               'pop_list': pop_list
               }
    return render(request, 'polls/setor_layout.html', context)

def evento_pc(request, id):
    ponto_controle = Ponto_Controle.objects.get(codigo=id)
    setor = Setor.objects.get(codigo=ponto_controle.idsetor)
    eventos_list = Ponto_Controle_Evento.objects.filter(codigo_pc=ponto_controle.codigo)
    campos_list1 = ponto_controle.campos.split('<')
    campos_list = []
    for linha in campos_list1:
        if linha.__contains__('Ponto_Controle_Campos'):
            campos_list.append(
                linha.replace('Ponto_Controle_Campos:', '').replace('>', '').replace(',', '').replace(']', '').replace(
                    ' ', ''))

    context = {'ponto_controle': ponto_controle,
               'setor': setor,
               'eventos_list': eventos_list,
               'campos_list': campos_list}
    return render(request, 'polls/evento_pc.html', context)


# forms
def evento_pc_form(request):
    if request.method == "POST":
        form = CarteiraForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('carteira'))
        else:
            menssagem = 'Ocorreu um erro!<br>' + str(form)
            return erro(request, menssagem)
    else:
        form = CarteiraForm()
        context = {'form': form}
        return render(request, 'polls/forms/evento_pc_form.html', context)

def layout_form(request,codigo):
    setor = Setor.objects.get(codigo=codigo)
    subsetor_list = SubSetor.objects.filter(idsetor=codigo).order_by('nome')
    pop_list = POP.objects.filter(codsetor=codigo).order_by('tarefa')
    setor_anos_list = ProducaoSetor.objects.raw(
        'SELECT strftime(\'%Y\',data) as ano,id from polls_producaosetor where cod_setor=\'' + codigo + '\' group by 1 order by 1 desc',
        translations={'ano': 'ano', 'id': 'id'})
    pontoscontrole_list = Ponto_Controle.objects.filter(idsetor=codigo).order_by('descricao')

    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        fs.delete('polls/static/polls/layouts/'+setor.codigo+'.jpg')
        filename = fs.save('polls/static/polls/layouts/'+setor.codigo+'.jpg', myfile)


        return HttpResponseRedirect('../setor_layout/' + str(codigo))

    else:
        context = {'setor': setor,
                   'subsetor_list': subsetor_list,
                   'anos_list': setor_anos_list,
                   'meses_list': meses(),
                   'pontoscontrole_list': pontoscontrole_list,
                   'pop_list': pop_list
                   }
    return render(request, 'polls/forms/layout_form.html', context)

def fluxograma_form(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save('polls/static/polls/fluxograma/'+myfile.name, myfile)
        return HttpResponseRedirect(reverse('fluxograma'))
    else:
        context = {}
    return render(request, 'polls/forms/fluxograma_form.html', context)

def imgpop_form(request,id,idsec):
    if request.method == 'POST':
        if request.FILES.__contains__('myfile'):
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            fs.delete('polls/static/polls/pop/'+str(id)+'.jpg')
            filename = fs.save('polls/static/polls/pop/'+str(id)+'.jpg', myfile)
        else:
            fs = FileSystemStorage()
            fs.delete('polls/static/polls/pop/' + str(id) + '.jpg')
        return HttpResponseRedirect('../../pop_det/'+str(idsec))
    else:
        procedimento = Procedimento.objects.get(id=id)
        tarefa = Tarefa.objects.get(id=procedimento.codigo_tarefa)
        context = {'id':idsec,
                   'tarefa': tarefa.codigo,
                   'procedimento': procedimento}
    return render(request, 'polls/forms/imgpop_form.html', context)

def carteira_form(request):
    if request.method == "POST":
        form = CarteiraForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('carteira'))
        else:
            menssagem = 'Ocorreu um erro!<br>' + str(form)
            return erro(request, menssagem)
    else:
        form = CarteiraForm()
        empresa_list = Empresa.objects.all()
        context = {'form': form,
                   'empresa_list': empresa_list}
        return render(request, 'polls/forms/carteira_form.html', context)

def devolucao_form(request):
    if request.method == "POST":
        form = DevolucaoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('devolucao'))
        else:
            menssagem = 'Ocorreu um erro!<br>' + str(form)
            return erro(request, menssagem)
    else:
        empresa_list = Empresa.objects.order_by('nome')
        form = DevolucaoForm()
        context = {'empresa_list': empresa_list
            , 'form': form
                   }
        return render(request, 'polls/forms/devolucao_form.html', context)

def faturamento_form(request):
    if request.method == "POST":
        form = FaturamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('faturamento'))
        else:
            menssagem = 'Ocorreu um erro!<br>' + str(form)
            return erro(request, menssagem)
    else:
        form = FaturamentoForm()
        context = {'form': form}
        return render(request, 'polls/forms/faturamento_form.html', context)

def prazoentrega_form(request):
    if request.method == "POST":
        form = PrazoEntregaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('prazoentrega'))
        else:
            menssagem = 'Ocorreu um erro!<br>' + str(form)
            return erro(request, menssagem)
    else:
        form = PrazoEntregaForm()
        context = {'form': form}
        return render(request, 'polls/forms/prazoentrega_form.html', context)

def producaosetor_form(request, id):
    if request.method == "POST":
        form = ProducaoSetorForm(request.POST)
        if form.is_valid():
            form.save(id)
            return HttpResponseRedirect(reverse('setor', kwargs={'id': id}))
        else:
            menssagem = 'Ocorreu um erro!<br>' + str(form)
            return erro(request, menssagem)
    else:
        form = ProducaoSetorForm()
        list_s = Setor.objects.order_by('codigo')
        for obj in list_s:
            if obj.codigo == id:
                setor = obj
        context = {'form': form,
                   'setor': setor, }
        return render(request, 'polls/forms/producaosetor_form.html', context)

def reprogramacaoretrabalho_form(request):
    if request.method == "POST":
        form = ReprogramacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('reprogramacaoretrabalho'))
        else:
            menssagem = 'Ocorreu um erro!<br>' + str(form)
            return erro(request, menssagem)
    else:
        form = ReprogramacaoForm()
        context = {'form': form}
        return render(request, 'polls/forms/reprogramacaoretrabalho_form.html', context)

# Historico
def setor_his(request, id, ano, mes):
    data = datetime.datetime(int(ano), int(mes), 1)
    anomes = str(ano) + '-' + str(mes)

    lista_s = Setor.objects.order_by('codigo')
    for obj in lista_s:
        if obj.codigo == id:
            setor = obj
    ultimo_dia = calendar.monthlen(2020, 8) + 1
    dias_mes_list = []
    for i in range(1, ultimo_dia):
        dias_mes_list.append(i)

    producao_atual_list = ProducaoSetor.objects.raw('SELECT '
                                                    'CAST(strftime(\'%d\',p.data) AS INT) as dia,'
                                                    'cast(sum(quantidade) as int) as quantidade, p.id '
                                                    'FROM polls_producaosetor as p '
                                                    'where strftime(\'%Y-%m\',p.data)=\'' + anomes + '\'  '
                                                                                                     'and p.cod_setor=\'' + id + '\''
                                                                                                                                 'group by 1 '
                                                                                                                                 'order by 1',
                                                    translations={'id': 'id',
                                                                  'dia': 'dia',
                                                                  'quantidade': 'quantidade'})

    reprogramacao_atual_list = ProducaoSetor.objects.raw('SELECT '
                                                         'CAST(strftime(\'%d\',p.data) AS INT) as dia,'
                                                         'sum(quantidade) as quantidade, p.id '
                                                         'FROM polls_reprogramacao as p '
                                                         'where strftime(\'%Y-%m\',p.data)=\'' + anomes + '\' '
                                                                                                          'and p.idsetor=\'' + id + '\' and p.retrabalho=0 '
                                                                                                                                    'group by 1 '
                                                                                                                                    'order by 1',
                                                         translations={'id': 'id',
                                                                       'dia': 'dia',
                                                                       'quantidade': 'quantidade'})

    retrabalho_atual_list = ProducaoSetor.objects.raw('SELECT '
                                                      'CAST(strftime(\'%d\',p.data) AS INT) as dia,'
                                                      'cast(sum(quantidade) as int) as quantidade, p.id '
                                                      'FROM polls_reprogramacao as p '
                                                      'where strftime(\'%Y-%m\',p.data)=\'' + anomes + '\' '
                                                                                                       'and p.idsetor=\'' + id + '\' and p.retrabalho=1 '
                                                                                                                                 'group by 1 '
                                                                                                                                 'order by 1',
                                                      translations={'id': 'id',
                                                                    'dia': 'dia',
                                                                    'quantidade': 'quantidade'})

    retrabalho_list = ProducaoSetor.objects.raw('SELECT '
                                                'm.descricao, '
                                                '\'\'||cast(sum(r.quantidade) as int) as quantidade, '
                                                'sum(r.custo) as custo, '
                                                'r.id '
                                                'FROM polls_reprogramacao as r '
                                                'INNER JOIN polls_motivo_reprogramacao m on m.idmotivo=r.idmotivo '
                                                'WHERE strftime(\'%Y-%m\',r.data)=\'' + anomes + '\' '
                                                                                                 'and r.idsetor=\'' + id + '\' '
                                                                                                                           'and retrabalho = 1  '
                                                                                                                           'group by 1 order by 3 desc'
                                                , translations={'id': 'id',
                                                                'ddescricao': 'descricao',
                                                                'quantidade': 'quantidade',
                                                                'custo': 'custo'})

    reprogramacao_list = ProducaoSetor.objects.raw('SELECT '
                                                   'm.descricao,'
                                                   '\'\'||Cast(sum(r.quantidade) as int) as quantidade,'
                                                   'sum(r.custo) as custo,'
                                                   'r.id '
                                                   'FROM polls_reprogramacao as r '
                                                   'INNER JOIN polls_motivo_reprogramacao m on m.idmotivo=r.idmotivo '
                                                   'WHERE strftime(\'%Y-%m\',r.data)=\'' + anomes + '\' '
                                                                                                    'and r.idsetor=\'' + id + '\' '
                                                                                                                              'and retrabalho = 0  '
                                                                                                                              'group by 1 order by 3 desc '
                                                   , translations={'id': 'id',
                                                                   'ddescricao': 'descricao',
                                                                   'quantidade': 'quantidade',
                                                                   'custo': 'custo'})

    pecas_reprogramadas = 0;
    custo_total_rep = 0;
    for obj in reprogramacao_list:
        pecas_reprogramadas += int(obj.quantidade)
        custo_total_rep += obj.custo

    pecas_retrabalhadas = 0;
    custo_total_ret = 0;
    for obj in retrabalho_list:
        pecas_retrabalhadas += int(obj.quantidade)
        custo_total_ret += obj.custo

    situaca_graf_list = []

    class objvalorgraf():
        dia = '0'
        prod = 0
        rep = 0
        ret = 0

    pecas_produzidas = 0;
    for dia in dias_mes_list:
        prod = 0
        rep = 0
        ret = 0

        for pr in producao_atual_list:
            if pr.dia == dia:
                prod = pr.quantidade

        for rp in reprogramacao_atual_list:
            if rp.dia == dia:
                rep = rp.quantidade

        for rt in retrabalho_atual_list:
            if rt.dia == dia:
                ret = rt.quantidade

        if prod > 0 or rep > 0 or ret > 0:
            valores = objvalorgraf()
            valores.dia = dia
            valores.prod = str(prod).replace(',', '')
            valores.rep = str(rep).replace(',', '')
            valores.ret = str(ret).replace(',', '')
            situaca_graf_list.append(
                "x: " + str(dia) + ", y: " + str(prod).replace(',', '') + ", z: " + str(ret).replace(',',
                                                                                                     '') + ", w: " + str(
                    rep).replace(',', ''))
        pecas_produzidas += prod

    titulo1 = setor.nome + " - " + data.strftime("%B/%Y")
    titulo2 = data.strftime("%B/%Y")
    titulo3 = data.strftime("%B %Y")

    context = {'setor': setor,
               'dias': dias_mes_list,
               'producao_atual_list': producao_atual_list,
               'reprogramacao_atual_list': reprogramacao_atual_list,
               'retrabalho_atual_list': retrabalho_atual_list,
               'situaca_graf_list': situaca_graf_list,
               'reprogramacao_list': reprogramacao_list,
               'retrabalho_list': retrabalho_list,
               'pecas_reprogramadas': pecas_reprogramadas,
               'pecas_retrabalhadas': pecas_retrabalhadas,
               'pecas_produzidas': pecas_produzidas,
               'custo_total_rep': custo_total_rep,
               'custo_total_ret': custo_total_ret,
               'data': data
               }
    return render(request, 'polls/historico/setor_his.html', context)

def reprogramacao_his(request, ano, mes):
    data = datetime.datetime(int(ano), int(mes), 1)
    empresa_list = Empresa.objects.order_by('nome')
    setor_list = Setor.objects.order_by('nome')
    relatorio_list = Relatorio.objects.order_by('descricao')

    reprogramacao_atual_list = Reprogramacao.objects.raw('SELECT '
                                                         't.*,round((custo*100/(select sum(f.faturamento) from polls_faturamento as f where f.idempresa=t.idempresa and t.ano = strftime(\'%Y\',f.data)  and strftime(\'%m\',DATE(\'NOW\')) = strftime(\'%m\',f.data))),1) as indice '
                                                         'FROM (SELECT r.id,'
                                                         'strftime(\'%Y\',r.data) as ano,'
                                                         'strftime(\'%d\',r.data) as dia,'
                                                         'r.idempresa,'
                                                         'case when r.retrabalho=1 then \'Retrabalho\' else \'Reprogramacao\' end as tipo,'
                                                         'SUM(r.quantidade) as quantidade,'
                                                         'round(SUM(r.custo),2) AS custo '
                                                         'FROM polls_reprogramacao as r '
                                                         'WHERE strftime(\'%Y\',r.data)=\'' + ano + '\' '
                                                                                                    'and strftime(\'%m\',r.data)=\'' + mes + '\' GROUP BY 2,3,4,5) as T',
                                                         translations={'id': 'id',
                                                                       'ano': 'ano',
                                                                       'dia': 'dia',
                                                                       'idempresa': 'idempresa',
                                                                       'tipo': 'tipo',
                                                                       'quantidade': 'quantidade',
                                                                       'custo': 'custo',
                                                                       'indice': 'indice'})

    reprogramacao_historico_list = Reprogramacao.objects.raw('SELECT '
                                                             't.*,round((custo*100/(select sum(f.faturamento) from polls_faturamento as f where f.idempresa=t.idempresa and t.ano = strftime(\'%Y\',f.data)  and t.mes = strftime(\'%m\',f.data))),2) as indice '
                                                             'FROM (SELECT r.id,'
                                                             'strftime(\'%Y\',r.data) as ano,'
                                                             'strftime(\'%m\',r.data) as mes,'
                                                             'r.idempresa,'
                                                             'case when r.retrabalho=1 then \'Retrabalho\' else \'Reprogramacao\' end as tipo,'
                                                             'cast(SUM(r.quantidade) as integer) as quantidade,'
                                                             'round(SUM(r.custo),2) AS custo '
                                                             'FROM polls_reprogramacao as r '
                                                             'GROUP BY 2,3,4,5 order by 2,3) as T ',
                                                             translations={'id': 'id',
                                                                           'ano': 'ano',
                                                                           'mes': 'mes',
                                                                           'idempresa': 'idempresa',
                                                                           'tipo': 'tipo',
                                                                           'quantidade': 'quantidade',
                                                                           'custo': 'custo',
                                                                           'indice': 'indice'})

    reprogramacao_grafico_list = Reprogramacao.objects.raw('SELECT e.id,'
                                                           'e.idempresa '
                                                           ',e.apelido as nome, e.nome as indice'
                                                           ', \'\'||Cast(coalesce(( '
                                                           'SELECT '
                                                           'sum(r.custo) from polls_reprogramacao as r '
                                                           'where strftime(\'%Y\',r.data)=\'' + ano + '\' '
                                                                                                      'and strftime(\'%m\',r.data)=\'' + mes + '\' '
                                                                                                                                               'and r.idempresa=e.idempresa '
                                                                                                                                               'and r.retrabalho=0 '
                                                                                                                                               ' ),0)as integer ) as reprogramacao '
                                                                                                                                               ',\'\'||Cast(coalesce(( '
                                                                                                                                               'SELECT '
                                                                                                                                               'sum(r.custo) from polls_reprogramacao as r '
                                                                                                                                               'where strftime(\'%Y\',r.data)=\'' + ano + '\' '
                                                                                                                                                                                          'and strftime(\'%m\',r.data)=\'' + mes + '\' '
                                                                                                                                                                                                                                   'and r.idempresa=e.idempresa '
                                                                                                                                                                                                                                   'and r.retrabalho=1 '
                                                                                                                                                                                                                                   '),0) as integer ) as retrabalho '
                                                                                                                                                                                                                                   ',coalesce((select '
                                                                                                                                                                                                                                   'sum(f.faturamento) from polls_faturamento as f '
                                                                                                                                                                                                                                   'where f.idempresa=e.idempresa '
                                                                                                                                                                                                                                   'and strftime(\'%Y\',f.data) = \'' + ano + '\'  '
                                                                                                                                                                                                                                                                              'and strftime(\'%m\',f.data) = \'' + mes + '\'),0) as faturamento '
                                                                                                                                                                                                                                                                                                                         'FROM polls_empresa as e '
                                                                                                                                                                                                                                                                                                                         'ORDER by 4',
                                                           translations={'id': 'id',
                                                                         'idempresa': 'idempresa',
                                                                         'nome': 'nome',
                                                                         'reprogramacao': 'reprogramacao',
                                                                         'retrabalho': 'retrabalho',
                                                                         'faturamento': 'faturamento'})

    context = {'empresa_list': empresa_list,
               'setor_list': setor_list,
               'relatorio_list': relatorio_list,
               'reprogramacao_atual_list': reprogramacao_atual_list,
               'data': data,
               'reprogramacao_historico_list': reprogramacao_historico_list,
               'reprogramacao_grafico_list': reprogramacao_grafico_list}
    return render(request, 'polls/historico/reprogramacao_his.html', context)

def producaogeral_his(request, ano, mes):
    data = datetime.datetime(int(ano), int(mes), 1)
    setor_list = Setor.objects.order_by('nome')
    ultimo_dia = calendar.monthlen(2020, 8) + 1
    dias_mes_list = []
    for i in range(1, ultimo_dia):
        dias_mes_list.append(i)

    producao_atual_list = ProducaoSetor.objects.raw(
        'SELECT p.id, cast(strftime(\'%d\', p.data) as integer) as dia, s.codigo, s.nome, '
        'cast(sum(p.quantidade) as integer) as quantidade FROM polls_producaosetor as p '
        'inner join polls_setor s on trim(s.codigo) = trim(p.cod_setor) '
        'WHERE strftime(\'%Y\', p.data) = \'' + ano + '\' and strftime(\'%m\', p.data) = \'' + mes + '\' '
                                                                                                     'group by 2, 3, 4 order by 2, 4 ',
        translations={'id': 'id', 'dia': 'dia', 'codigo': 'codigo', 'nome': 'nome', 'quantidade': 'quantidade'})

    producao_atual_grafica = ProducaoSetor.objects.raw(
        'SELECT p.id,s.nome,\'\'||(cast(SUM(p.quantidade) as int)) as quantidade '
        'FROM polls_producaosetor as p '
        'inner join polls_setor s on trim(s.codigo)=trim(p.cod_setor) '
        'WHERE strftime(\'%Y\',p.data)=\'' + ano + '\' '
                                                   'and strftime(\'%m\',p.data)=\'' + mes + '\' '
                                                                                            'group by 2 order by 2',
        translations={'id': 'id', 'nome': 'nome', 'quantidade': 'quantidade'})
    producao_atual_total = ProducaoSetor.objects.raw(
        'SELECT p.id,\'\'||coalesce(cast(sum(p.quantidade)as int),0) as quantidade FROM polls_producaosetor as p '
        'inner join polls_setor s on trim(s.codigo)=trim(p.cod_setor) '
        'WHERE strftime(\'%Y\',p.data)=\'' + ano + '\' '
                                                   'and strftime(\'%m\',p.data)=\'' + mes + '\' ',
        translations={'id': 'id', 'quantidade': 'quantidade'})

    total_mes = ''
    for objeto in producao_atual_total:
        total_mes = objeto.quantidade

    context = {
        'setor_list': setor_list,
        'dias_mes_list': dias_mes_list,
        'producao_atual_list': producao_atual_list,
        'producao_atual_grafica': producao_atual_grafica,
        'total_mes': total_mes,
        'data': data}
    return render(request, 'polls/historico/producaogeral_his.html', context)

def prazoentrega_his(request, ano, mes):
    data = datetime.datetime(int(ano), int(mes), 1)
    linhas_producao_list = LinhaProducao.objects.order_by('descricao')

    prazo_atual_list = PrazoEntrega.objects.raw('SELECT '
                                                'strftime(\'%Y\',p.data)||\'-\'||strftime(\'%m\',p.data)||\'-01\' as data, '
                                                'l.descricao, '
                                                'avg(p.prazo) as prazo, p.id as id '
                                                'from polls_prazoentrega as p '
                                                'inner join polls_linhaproducao l on l.codigo1=p.linhaproducao '
                                                'where strftime(\'%Y\',p.data)=\'' + ano + '\' AND strftime(\'%m\',p.data)=\'' + mes + '\' '
                                                                                                                                       'group by 1,2 '
                                                                                                                                       'order by 2 ',
                                                translations={'id': 'id', 'data': 'data', 'descricao': 'descricao',
                                                              'prazo': 'prazo'})

    context = {'prazo_atual_list': prazo_atual_list,
               'linhas_producao_list': linhas_producao_list,
               'data': data}
    return render(request, 'polls/historico/prazoentrega_his.html', context)

def faturamento_his(request, ano, mes):
    data = datetime.datetime(int(ano), int(mes), 1)
    empresa_list = Empresa.objects.order_by('nome')
    relatorio_list = Relatorio.objects.order_by('descricao')[:5]

    faturamento_atual_list = Faturamento.objects.filter(data__year=data.year, data__month=data.month)
    faturamento_anos_list = Faturamento.objects.raw(
        'SELECT strftime(\'%Y\',data) as ano,id from polls_faturamento group by 1 order by 1 desc',
        translations={'ano': 'ano', 'id': 'id'})

    faturamento_atual_total_list = Carteira.objects.raw(
        'select idempresa,\'\'||cast(sum(faturamento) as int) as valor, id from polls_faturamento '
        'WHERE strftime(\'%Y\',data)=\'' + ano + '\' '
                                                 'and strftime(\'%m\',data)=\'' + mes + '\' '
                                                                                        ' group by 1',
        translations={'id': 'id', 'idempresa': 'idempresa', 'valor': 'valor'})
    ultimo_dia = calendar.monthlen(datetime.datetime.now().year, datetime.datetime.now().month) + 1
    dias_mes_list = []
    for i in range(1, ultimo_dia):
        dias_mes_list.append(i)

    faturamento_graf_mes_list = []
    for dia in dias_mes_list:
        dd = str(dia)
        dados = []
        dados.append(dd)
        for empresa in empresa_list:
            temp = 0
            for fat in faturamento_atual_list:
                if fat.idempresa == empresa.idempresa and dia == int(fat.data.strftime("%d")):
                    temp = str(fat.faturamento)
            dados.append(temp)
        if len(dados) == 1:
            faturamento_graf_mes_list.append("x: " + dados[0] + ", y: 0, z: 0, w: 0")
        elif len(dados) == 2:
            faturamento_graf_mes_list.append("x: " + dados[0] + ", y: " + str(dados[1]) + ", z: 0, w: 0")
        elif len(dados) == 3:
            faturamento_graf_mes_list.append(
                "x: " + dados[0] + ", y: " + str(dados[1]) + ", z: " + str(dados[2]) + ", w: 0")
        elif len(dados) == 4:
            faturamento_graf_mes_list.append(
                "x: " + dados[0] + ", y: " + str(dados[1]) + ", z: " + str(dados[2]) + ", w: " + str(dados[3]))

    context = {'empresa_list': empresa_list,
               'relatorio_list': relatorio_list,
               'faturamento_atual_list': faturamento_atual_list,
               'faturamento_anos_list': faturamento_anos_list,
               'faturamento_atual_total_list': faturamento_atual_total_list,
               'dias_mes_list': dias_mes_list,
               'data': data,
               'faturamento_graf_mes_list': faturamento_graf_mes_list}
    return render(request, 'polls/historico/faturamento_his.html', context)

def devolucao_his(request, ano, mes):
    data = datetime.datetime(int(ano), int(mes), 1)
    empresa_list = Empresa.objects.order_by('nome')[:5]

    devolucao_atual_list = Devolucao.objects.filter(data_devolucao__year=int(ano),
                                                    data_devolucao__month=int(mes)).order_by('data_devolucao')
    devolucao_atual_valor_list = Devolucao.objects.raw(
        'SELECT idempresa, \'\'||(cast(SUM(VALOR) as int)) AS valor, id FROM polls_devolucao '
        'WHERE strftime(\'%Y\',data_devolucao)=\'' + str(data.date().year) + '\' '
                                                                             'AND strftime(\'%m\',data_devolucao)=\'' + mes + '\' '
                                                                                                                              'GROUP BY IDEMPRESA',
        translations={'idempresa': 'idempresa', 'valor': 'valor', 'id': 'id'})

    devolucao_anos_list = Devolucao.objects.raw(
        'SELECT strftime(\'%Y\',data_devolucao) as ano,id from polls_devolucao group by 1 order by 1 desc',
        translations={'ano': 'ano', 'id': 'id'})

    relatorio_list = Relatorio.objects.order_by('descricao')[:5]
    context = {'empresa_list': empresa_list,
               'relatorio_list': relatorio_list,
               'devolucao_atual_list': devolucao_atual_list,
               'devolucao_atual_valor_list': devolucao_atual_valor_list,
               'devolucao_anos_list': devolucao_anos_list,
               'data': data}
    return render(request, 'polls/historico/devolucao_his.html', context)

def carteira_his(request, ano, mes):
    data = datetime.datetime(int(ano), int(mes), 1)
    anomes = str(ano) + '' + str(mes)

    carteira_dias_list = Carteira.objects.raw(
        'SELECT strftime(\'%d\',data) as ano,id from polls_carteira where  strftime(\'%Y%m\',data) = \'' + anomes + '\' group by 1 order by 1 ',
        translations={'dias': 'dias', 'id': 'id'})

    carteira_atual_list = Carteira.objects.filter(data__year=int(ano),
                                                  data__month=int(mes)).order_by('data')
    carteira_atual_valor_list = Carteira.objects.raw('SELECT '
                                                     'e.nome as apelido,e.idempresa,'
                                                     '\'\'||coalesce((select f.carteira from polls_carteira as f where f.idempresa=e.idempresa and strftime(\'%Y%m\',f.data)=\'' + anomes + '\' order by data desc limit 1),0) as valor,'
                                                                                                                                                                                            'e.id '
                                                                                                                                                                                            'from polls_empresa as e order by 1',
                                                     translations={'idempresa': 'idempresa', 'apelido': 'apelido',
                                                                   'valor': 'valor', 'id': 'id'})

    empresa_list = Empresa.objects.order_by('nome')

    faturamento_total_list = Faturamento.objects.raw('select '
                                                     'idempresa,sum(faturamento ) as valor,id '
                                                     'from polls_faturamento '
                                                     'where  strftime(\'%Y%m\',data) = \'' + anomes + '\' '
                                                                                                      'group by 1',
                                                     translations={'id': 'id', 'idempresa': 'idempresa',
                                                                   'valor': 'valor'})

    class giroCarteira:
        idempresa = 0
        giro = 0

    list_giro = []
    for obj in faturamento_total_list:
        for obj1 in carteira_atual_valor_list:
            if obj.idempresa == obj1.idempresa:
                objg = giroCarteira()
                objg.idempresa = obj.idempresa
                objg.giro = (obj.valor / int(obj1.valor))
                list_giro.append(objg)

    context = {'empresa_list': empresa_list,
               'data': data,
               'carteira_atual_valor_list': carteira_atual_valor_list,
               'carteira_atual_list': carteira_atual_list,
               'list_giro': list_giro,
               'carteira_dias_list': carteira_dias_list}
    return render(request, 'polls/historico/carteira_his.html', context)


# Admin
def admin(request):
    context = {}
    return render(request, 'polls/admin.html', context)

def empresa_list(request):
    objeto_list = Empresa.objects.order_by('nome')
    context = {'objeto_list': objeto_list}
    return render(request, 'polls/empresa_list.html', context)

def usuario_list(request):
    objeto_list = User.objects.all().order_by('first_name')
    #User.groups.all()
    context = {'objeto_list': objeto_list}
    return render(request, 'polls/usuario_list.html', context)

def linhaproducao_list(request):
    objeto_list = LinhaProducao.objects.order_by('descricao')
    context = {'objeto_list': objeto_list}
    return render(request, 'polls/linhaproducao_list.html', context)

def motivoreprogramacao_list(request):
    objeto_list = Motivo_reprogramacao.objects.order_by('descricao')
    context = {'objeto_list': objeto_list}
    return render(request, 'polls/motivoreprogramacao_list.html', context)

def pontocontrole_list(request):
    objeto_list = Ponto_Controle.objects.raw('SELECT '
                                             '(CASE '
                                             'when e.idempresa<>\'\' then s.nome||\'(\'||e.apelido||\')\' '
                                             'else s.nome end ) as setor,'
                                             'p.idsetor as idsetor,'
                                             'p.codigo as codigo,'
                                             'p.descricao,'
                                             'replace(p.campos,\'<QuerySet [\',\'\') as campos,p.id '
                                             'FROM polls_ponto_controle as p '
                                             'LEFT JOIN polls_setor s ON s.codigo=p.idsetor '
                                             'LEFT JOIN polls_empresa e ON s.idempresa=e.idempresa '
                                             'order by 1,2',
                                             translations={'id': 'id', 'setor': 'setor', 'idsetor': 'idsetor',
                                                           'codigo': 'codigo',
                                                           'descricao': 'descricao', 'campos': 'campos'})
    for obj in objeto_list:
        obj.campos = str(obj.campos).replace('<Ponto_Controle_Campos: ', '').replace('>', '').replace(']', '')
    context = {'objeto_list': objeto_list}
    return render(request, 'polls/pontocontrole_list.html', context)

def setor_list(request):
    objeto_list = Setor.objects.raw('select '
                                    's.codigo,'
                                    '(CASE'
                                    ' when e.apelido is null THEN s.nome '
                                    'ELSE '
                                    '	s.nome||\' (\' || e.apelido||\')\' '
                                    'END) as nome,s.id '
                                    'from polls_setor as s '
                                    'left join polls_empresa e on e.idempresa=s.idempresa order by 2',
                                    translations={'id': 'id', 'codigo': 'codigo', 'nome': 'nome'})
    context = {'objeto_list': objeto_list}
    return render(request, 'polls/setor_list.html', context)

def subsetor_list(request):
    objeto_list = SubSetor.objects.raw('SELECT '
                                       '(CASE '
                                       'when e.idempresa<>\'\' then s.nome||\'(\'||e.apelido||\')\' '
                                       'else s.nome end ) as setor,'
                                       'p.idsetor as idsetor,'
                                       'p.codigo as codigo,'
                                       'p.nome, p.id '
                                       'FROM polls_subsetor as p '
                                       'LEFT JOIN polls_setor s ON s.codigo=p.idsetor '
                                       'LEFT JOIN polls_empresa e ON s.idempresa=e.idempresa '
                                       'order by 1,2',
                                       translations={'id': 'id', 'setor': 'setor', 'idsetor': 'idsetor',
                                                     'codigo': 'codigo',
                                                     'nome': 'nome'})
    context = {'objeto_list': objeto_list}
    return render(request, 'polls/subsetor_list.html', context)

def materiaprima_list(request):
    objeto_list = MateriaPrima.objects.order_by('descricao')
    context = {'objeto_list': objeto_list}
    return render(request, 'polls/materiaprima_list.html', context)

def operador_list(request):
    objeto_list = Operador.objects.order_by('nome')
    context = {'objeto_list': objeto_list}
    return render(request, 'polls/operador_list.html', context)

def processo_list(request):
    objeto_list = Processo.objects.raw('SELECT '
                                       'e.apelido as empresa, '
                                       's.nome as setor, '
                                       'p.codigo, '
                                       'p.descricao, '
                                       '0 as tempo_medio, p.id  '
                                       'FROM polls_processo as p '
                                       'LEFT JOIN polls_setor s ON s.codigo=p.idsetor '
                                       'LEFT JOIN polls_empresa e ON s.idempresa=e.idempresa '                                       
                                       'order by 1,3',
                                       translations={'empresa':'empresa',
                                                     'setor': 'setor',
                                                     'codigo': 'codigo',
                                                     'descricao': 'descricao',
                                                     'tempo_medio': 'tempo_medio',
                                                     'id': 'id'})
    context = {'objeto_list': objeto_list}
    return render(request, 'polls/processo_list.html', context)

def pop_list(request):
    objeto_list = POP.objects.raw('SELECT '
                                  'p.codigo,'
                                  '(CASE '
                                  '	WHEN e.idempresa is not null then \'(\'||e.apelido||\')\'||s.nome '
                                  '	ELSE s.nome '
                                  '	end ) as setor,'
                                  'ss.nome as subsetor, '
                                  'p.tarefa,'
                                  'p.revisao,'
                                  'p.revisor,'
                                  'p.data, p.id '
                                  'FROM polls_pop as p '
                                  'LEFT JOIN polls_setor s on s.codigo=trim(p.codsetor) '
                                  'LEFT JOIN polls_empresa e on s.idempresa=e.idempresa '
                                  'LEFT JOIN polls_subsetor ss on ss.codigo=p.codsubsetor '
                                  'order by 2,1 ',
                                  translations={'id': 'id',
                                                'codigo': 'codigo',
                                                'setor': 'setor',
                                                'subsetor': 'subsetor',
                                                'tarefa': 'tarefa',
                                                'revisao': 'revisao',
                                                'revisor': 'revisor',
                                                'data': 'data'})
    context = {'objeto_list': objeto_list}
    return render(request, 'polls/pop_list.html', context)

def pop_det(request,id):
    pop = POP.objects.get(id=id)
    setor = Setor.objects.get(codigo=pop.codsetor)
    subsetor = SubSetor.objects.get(codigo=pop.codsubsetor)
    tarefa_list = Tarefa.objects.filter(codigo_pop=pop.codigo).order_by('codigo')
    procedimento_list = Procedimento.objects.raw('SELECT '
                                                 'o.id as idpop, '
                                                 't.codigo as codtarefa, '
                                                 'p.id, '
                                                 'p.codigo, '
                                                 'p.codigo_tarefa, '
                                                 'p.descricao, '
                                                 'p.observacao '
                                                 'FROM polls_pop as o '
                                                 'LEFT JOIN polls_tarefa t on t.codigo_pop=o.codigo '
                                                 'LEFT JOIN polls_procedimento p on p.codigo_tarefa=t.id '
                                                 'WHERE o.id='+str(pop.id)+' and p.descricao is not NULL order by 4',
                                                 translations={'idpop':'idpop',
                                                               'codtarefa':'codtarefa',
                                                               'id':'id',
                                                               'codigo':'codigo',
                                                               'codigo_tarefa':'codigo_tarefa',
                                                               'descricao':'descricao',
                                                               'observacao':'observacao'})
    context = {'pop':pop,
               'setor':setor,
               'subsetor': subsetor,
               'tarefa_list': tarefa_list,
               'procedimento_list':procedimento_list
               }
    return render(request, 'polls/pop_det.html', context)

def pop_view(request,id):
    pop = POP.objects.get(id=id)
    setor = Setor.objects.get(codigo=pop.codsetor)
    subsetor = SubSetor.objects.get(codigo=pop.codsubsetor)
    subsetor_list = SubSetor.objects.filter(idsetor=setor.codigo).order_by('nome')
    pop_list = POP.objects.filter(codsetor=setor.codigo).order_by('tarefa')
    pontoscontrole_list = Ponto_Controle.objects.filter(idsetor=setor.codigo).order_by('descricao')
    setor_anos_list = ProducaoSetor.objects.raw(
        'SELECT strftime(\'%Y\',data) as ano,id from polls_producaosetor where cod_setor=\''+setor.codigo+'\' group by 1 order by 1 desc',
        translations={'ano': 'ano', 'id': 'id'})

    tarefa_list = Tarefa.objects.filter(codigo_pop=pop.codigo).order_by('codigo')
    procedimento_list = Procedimento.objects.raw('SELECT '
                                                 'o.id as idpop, '
                                                 't.codigo as codtarefa, '
                                                 'p.id, '
                                                 'p.codigo, '
                                                 'p.codigo_tarefa, '
                                                 'p.descricao, '
                                                 'p.observacao '
                                                 'FROM polls_pop as o '
                                                 'LEFT JOIN polls_tarefa t on t.codigo_pop=o.codigo '
                                                 'LEFT JOIN polls_procedimento p on p.codigo_tarefa=t.id '
                                                 'WHERE o.id='+str(pop.id)+' and p.descricao is not NULL order by 4',
                                                 translations={'idpop':'idpop',
                                                               'codtarefa':'codtarefa',
                                                               'id':'id',
                                                               'codigo':'codigo',
                                                               'codigo_tarefa':'codigo_tarefa',
                                                               'descricao':'descricao',
                                                               'observacao':'observacao'})

    context = {'pop':pop,
               'setor':setor,
               'subsetor': subsetor,
               'subsetor_list': subsetor_list,
               'pop_list': pop_list,
               'pontoscontrole_list':pontoscontrole_list,
               'anos_list':setor_anos_list,
               'cod_setor': setor.codigo,
               'meses_list': meses(),
               'tarefa_list': tarefa_list,
               'procedimento_list': procedimento_list
               }
    return render(request, 'polls/pop_view.html', context)

# Ferramentas
def matrizbcg(request):
    empresa_list = Empresa.objects.order_by('nome')[:5]
    setor_list = Setor.objects.order_by('nome')
    context = {'empresa_list': empresa_list,
               'setor_list': setor_list}
    return render(request, 'polls/ferramentas/matrizbcg.html', context)

def fluxograma(request):
    lis_dir = []

    for l in os.listdir('./polls/static/polls/fluxograma'):
        lis_dir.append(l)

    context = {'list_dir':lis_dir}
    return render(request, 'polls/ferramentas/fluxograma.html', context)

def folha_observacoes_list(request):
    folha_list = FolhaObservacao.objects.raw('SELECT '
                                             'f.id, '
                                             'f.folha, '
                                             'p.descricao as processo, '
                                             's.nome as setor, '
                                             'e.apelido as empresa '
                                             'FROM polls_folhaobservacao as f '
                                             'LEFT JOIN polls_processo p ON p.codigo=f.cod_processo '
                                             'LEFT JOIN polls_setor s ON s.codigo=p.idsetor '
                                             'LEFT join polls_empresa e ON e.idempresa=s.idempresa '
                                             'ORDER BY 5,4,3,2', translations={'id':'id',
                                                                               'folha':'folha',
                                                                               'processo':'processo',
                                                                               'setor':'setor',
                                                                               'empresa':'empresa'})
    context = {'folha_list':folha_list}
    return render(request, 'polls/ferramentas/folha_observacoes_list.html', context)

def folha_observacoes(request,id,alt):
    folha = FolhaObservacao.objects.get(id=id)
    elemento_list = FolhaElemento.objects.filter(id_folha=id).order_by('ordinal')
    tempo_list = ElementoTempo.objects.all().order_by('id_elemento')
    processo = Processo.objects.get(codigo=folha.cod_processo)

    class totalizacao:
        linha = 0
        valores = []

        def __init__(self, param1, param2):
            self.linha = param1
            self.valores = param2

    total_list = []

    indice = 0
    valort = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    linha = 0
    for tempo in tempo_list:
        if indice < 10:
            valort[indice] += tempo.tempo
            indice += 1
            linha = tempo.id_elemento
        else:
            val = valort.copy()
            total_list.append(totalizacao(linha,val))
            indice=0
            valort[indice] += tempo.tempo
            indice += 1

    total_list.append(totalizacao(linha,valort.copy()))

    tempo_percorrido = 0
    tempo_efetivo = 0
    unidades_acabadas = 0
    for val in valort:
        tempo_percorrido+=val
        tempo_efetivo+=val
        if val>0:
            unidades_acabadas +=1


    context = {'folha':folha,
               'elemento_list':elemento_list,
               'tempo_list': tempo_list,
               'processo':processo,
               'total_list':total_list,
               'tempo_percorrido': tempo_percorrido,
               'tempo_efetico': tempo_efetivo,
                'unidades_acabadas':unidades_acabadas,
               'alt':alt}
    return render(request, 'polls/ferramentas/folha_observacoes.html', context)

# Relatorios
def devolucao_rel(request, id, ano):
    titulo = ""
    titulo1 = ""
    titulotab = []
    tipo = []
    dados = []
    dados_graf = []
    devolucao_anos_list = Devolucao.objects.raw(
        'SELECT strftime(\'%Y\',data_devolucao) as ano,id from polls_devolucao group by 1 order by 1 desc',
        translations={'ano': 'ano', 'id': 'id'})
    devolucao_meses_list = Devolucao.objects.raw(
        'SELECT strftime(\'%m\',data_devolucao) as mes,id from polls_devolucao where strftime(\'%Y\',data_devolucao)=\'' + ano + '\' group by 1 order by 1 desc',
        translations={'ano': 'ano', 'id': 'id'})

    if id == 1:
        titulo = 'Devolução x Faturamento (' + ano + ')'
        titulo1 = 'Indice de Devolução x Faturamento'
        titulotab.append('Mês')
        titulotab.append('Devolução(R$)')
        titulotab.append('Faturamento(R$)')
        titulotab.append('Indice(%)')
        dados = Devolucao.objects.raw('SELECT '
                                      'T.mes,'
                                      'T.idempresa, '
                                      'T.devolucao, '
                                      'T.faturamento,t.id, '
                                      '((T.devolucao/T.faturamento)*100) as indice '
                                      'FROM '
                                      '(select '
                                      'strftime(\'%m\',d.data_devolucao) as mes, '
                                      'd.idempresa, '
                                      'e.apelido,d.id, '
                                      'sum(d.valor) as devolucao, '
                                      '(SELECT sum(faturamento) from polls_faturamento f where f.idempresa=d.idempresa and strftime(\'%Y%m\',d.data_devolucao)=strftime(\'%Y%m\',f.data))  as faturamento '
                                      'from polls_devolucao as d '
                                      'inner join polls_empresa e on e.idempresa=d.idempresa '
                                      'where strftime(\'%Y\',d.data_devolucao)=\'' + ano + '\' '
                                                                                           'group by 1,2,3 '
                                                                                           ') as T order by 1  ',
                                      translations={'mes': 'mes',
                                                    'idempresa': 'idempresa',
                                                    'devolucao': 'devolucao',
                                                    'faturamento': 'faturamento',
                                                    'indice': 'indice',
                                                    'id': 'id'})
    elif id == 2:
        titulo = 'Origem Devolução (' + ano + ')'
        titulo1 = 'Comparativo das Origens de Devoluções'
        titulotab.append('Mês')
        titulotab.append('Fábrica(R$)')
        titulotab.append('Representante(R$)')
        titulotab.append('Cliente(R$)')
        tipo.append('FABRICA')
        tipo.append('REPRESENTANTE')
        tipo.append('CLIENTE')
        dados = Devolucao.objects.raw('SELECT '
                                      'idempresa,'
                                      'strftime(\'%m\',data_devolucao) as mes,'
                                      'origem_erro,'
                                      'sum(valor) as valor, id '
                                      'FROM polls_devolucao '
                                      'WHERE strftime(\'%Y\',data_devolucao)=\'' + ano + '\' '
                                                                                         'group by 1,2,3 '
                                                                                         'order by 2,1',
                                      translations={'id': 'id', 'idempresa': 'idempresa', 'mes': 'mes',
                                                    'origem_erro': 'origem_erro', 'valor': 'valor'})

    dados_graf = Devolucao.objects.raw('SELECT '
                                       'strftime(\'%m\',data_devolucao) as mes,'
                                       'origem_erro,'
                                       '\'\'||cast(sum(valor) as int) as valor, id '
                                       'FROM polls_devolucao '
                                       'WHERE strftime(\'%Y\',data_devolucao)=\'' + ano + '\' '
                                                                                          'group by 1,2 '
                                                                                          'order by 1',
                                       translations={'id': 'id', 'idempresa': 'idempresa', 'mes': 'mes',
                                                     'origem_erro': 'origem_erro', 'valor': 'valor'})

    empresa_list = Empresa.objects.order_by('nome')
    context = {'empresa_list': empresa_list,
               'dados': dados,
               'dados_graf': dados_graf,
               'titulo': titulo,
               'titulo1': titulo1,
               'titulotab': titulotab,
               'tipos': tipo,
               'list_meses': meses(),
               'devolucao_anos_list': devolucao_anos_list,
               'devolucao_meses_list': devolucao_meses_list,
               'id': id}
    return render(request, 'polls/relatorios/devolucao_rel.html', context)


# Cadastros Alteração & Exclusao
def cadastros_form(request, id, codigo):
    if id == 1:
        if request.method == "POST":
            form = EmpresaForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('empresa_list'))
        else:
            form = EmpresaForm()
            context = {'tipo': 'Empresa', 'form': form}
    elif id == 2:
        if request.method == "POST":
            form = LinhaProducaoForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('linhaproducao_list'))
        else:
            form = LinhaProducaoForm()
            context = {'tipo': 'Linha de Produção', 'form': form}
    elif id == 3:
        if request.method == "POST":
            form = MotivoReprogramacaoForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('motivoreprogramacao_list'))
        else:
            form = MotivoReprogramacaoForm()
        context = {'tipo': 'Motivo Reprogramação/Retrabalho', 'form': form}
    elif id == 4:
        if request.method == "POST":
            form = PontoControleForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('pontocontrole_list'))
        else:
            ultimo_codigo = Ponto_Controle.objects.raw(
                'SELECT CAST(coalesce(max(codigo),0) as int) as ultimo,id from polls_ponto_controle ',
                translations={'ultimo': 'ultimo', 'id': 'id'})
            for ultimo in ultimo_codigo:
                proximo_codigo = '{:0>4}'.format(ultimo.ultimo + 1)

            form = PontoControleForm(initial={'codigo': proximo_codigo})
        context = {'tipo': 'Pontos de Controle', 'form': form}
    elif id == 5:
        if request.method == "POST":
            form = SetorForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('setor_list'))
        else:
            form = SetorForm()

        context = {'tipo': 'Setor', 'form': form}
    elif id == 6:
        if request.method == "POST":
            form = SubSetorForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('subsetor_list'))
        else:
            ultimo_codigo = SubSetor.objects.raw(
                'SELECT CAST(coalesce(max(codigo),0) as int) as ultimo,id from polls_subsetor ',
                translations={'ultimo': 'ultimo', 'id': 'id'})
            for ultimo in ultimo_codigo:
                proximo_codigo = '{:0>4}'.format(ultimo.ultimo + 1)
            form = SubSetorForm(initial={'codigo': proximo_codigo})

        context = {'tipo': 'Sub- Setor', 'form': form}
    elif id == 7:
        if request.method == "POST":
            form = MateriaPrimaForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('materiaprima_list'))
        else:
            form = MateriaPrimaForm()
        context = {'tipo': 'Materia Prima', 'form': form}
    elif id == 8:
        if request.method == "POST":
            form = OperadorForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('operador_list'))
        else:
            form = OperadorForm()
        context = {'tipo': 'Operador', 'form': form}
    elif id == 9:
        if request.method == "POST":
            form = ProcessoForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('processo_list'))
        else:
            form = ProcessoForm(initial={'tempo_medio': 0})
        context = {'tipo': 'Processo', 'form': form}
    elif id == 10:
        if request.method == "POST":
            form = PopForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('pop_list'))
        else:
            ultimo_codigo = SubSetor.objects.raw(
                'SELECT CAST(coalesce(max(codigo),0) as int) as ultimo,id from polls_pop ',
                translations={'ultimo': 'ultimo', 'id': 'id'})
            for ultimo in ultimo_codigo:
                proximo_codigo = '{:0>4}'.format(ultimo.ultimo + 1)
            form = PopForm(initial={'codigo': proximo_codigo})
        context = {'tipo': 'POP', 'form': form}
    elif id == 11:
        if request.method == "POST":
            form = TarefaForm(request.POST)
            if form.is_valid():
                form.save()
                pop = POP.objects.get(codigo=codigo)
                return HttpResponseRedirect('../../../pop_det/'+str(pop.id))
        else:
            form = TarefaForm(initial={'codigo_pop': codigo })
        context = {'tipo': 'Tarefa', 'form': form }
    elif id == 12:
        if request.method == "POST":
            form = ProcedimentoForm(request.POST)
            if form.is_valid():
                form.save()
                tarefa = Tarefa.objects.get(id=codigo)
                pop = POP.objects.get(codigo=tarefa.codigo_pop)
                return HttpResponseRedirect('../../../pop_det/' + str(pop.id))
        else:
            form = ProcedimentoForm(initial={'codigo_tarefa':codigo})
        context = {'tipo': 'Procedimento', 'form': form}
    elif id == 13:
        if request.method == "POST":
            form = UsuarioForm(request.POST)
            if form.is_valid():
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                idgrupo = request.POST['idgrupo']
                email = request.POST['email']
                password = request.POST['password1']
                form.save(first_name, last_name, email, idgrupo,password)
                return HttpResponseRedirect(reverse('usuario_list'))
        else:
            form =  UsuarioForm(initial={'username':'','password1':''})
        context = {'tipo': 'Usuario', 'form': form}
    elif id == 14:
        if request.method == "POST":
            form = FolhaObservacaoForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('folha_observacoes_list'))
        else:
            form =  FolhaObservacaoForm()
        context = {'tipo': 'Folha de Observação', 'form': form}
    elif id == 15:
        if request.method == "POST":
            form = FolhaElementoForm(request.POST)
            if form.is_valid():
                id_folha = request.POST['id_folha']
                ordinal = request.POST['ordinal']
                elemento = request.POST['elemento']
                velocidade = request.POST['velocidade']
                avanco = request.POST['avanco']
                t1 = request.POST['t1']
                t2 = request.POST['t2']
                t3 = request.POST['t3']
                t4 = request.POST['t4']
                t5 = request.POST['t5']
                t6 = request.POST['t6']
                t7 = request.POST['t7']
                t8 = request.POST['t8']
                t9 = request.POST['t9']
                t10 = request.POST['t10']
                form.save(ordinal,id_folha,elemento,velocidade,avanco,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10)
                return HttpResponseRedirect('../../../folha_observacoes/' + str(codigo) + '/1')
        else:
            form =  FolhaElementoForm(initial={'id_folha':codigo})
        context = {'tipo': 'Elemento da Folha de Observação', 'form': form}

    return render(request, 'polls/forms/cadastro_form.html', context)

def alteracao(request,id,pk):
    if id == 1:
        if request.method == "POST":
            obj = get_object_or_404(Empresa, id=pk)
            form = EmpresaForm(request.POST,instance=obj)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('empresa_list'))
            else:
                menssagem = 'Ocorreu um erro!<br>' + str(form)
                return erro(request, menssagem)
        else:
            obj = get_object_or_404(Empresa,id=pk)
            form = EmpresaForm(instance=obj)
            context = {'tipo': 'Empresa', 'form': form}
    elif id == 2:
        if request.method == "POST":
            obj = get_object_or_404(LinhaProducao, id=pk)
            form = LinhaProducaoForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('linhaproducao_list'))
            else:
                menssagem = 'Ocorreu um erro!<br>' + str(form)
                return erro(request, menssagem)
        else:
            obj = get_object_or_404(LinhaProducao, id=pk)
            form = LinhaProducaoForm(instance=obj)
            context = {'tipo': 'Linha de Produção', 'form': form}
    elif id == 3:
        if request.method == "POST":
            obj = get_object_or_404(Motivo_reprogramacao, id=pk)
            form = MotivoReprogramacaoForm(request.POST,instance=obj)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('motivoreprogramacao_list'))
            else:
                menssagem = 'Ocorreu um erro!<br>' + str(form)
                return erro(request, menssagem)
        else:
            obj = get_object_or_404(Motivo_reprogramacao, id=pk)
            form = MotivoReprogramacaoForm(instance=obj)
        context = {'tipo': 'Motivo Reprogramação/Retrabalho', 'form': form}
    elif id == 4:
        if request.method == "POST":
            obj = get_object_or_404(Ponto_Controle, id=pk)
            form = PontoControleForm(request.POST,instance=obj)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('pontocontrole_list'))
            else:
                menssagem = 'Ocorreu um erro!<br>' + str(form)
                return erro(request, menssagem)
        else:
            obj = get_object_or_404(Ponto_Controle, id=pk)
            form = PontoControleForm(instance=obj)
        context = {'tipo': 'Pontos de Controle', 'form': form}
    elif id == 5:
        if request.method == "POST":
            obj = get_object_or_404(Setor, id=pk)
            form = SetorForm(request.POST,instance=obj)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('setor_list'))
            else:
                menssagem = 'Ocorreu um erro!<br>' + str(form)
                return erro(request, menssagem)
        else:
            obj = get_object_or_404(Setor, id=pk)
            form = SetorForm(instance=obj)
        context = {'tipo': 'Setor', 'form': form}
    elif id == 6:
        if request.method == "POST":
            obj = get_object_or_404(SubSetor, id=pk)
            form = SubSetorForm(request.POST,instance=obj)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('subsetor_list'))
            else:
                menssagem = 'Ocorreu um erro!<br>' + str(form)
                return erro(request, menssagem)
        else:
            obj = get_object_or_404(SubSetor, id=pk)
            form = SubSetorForm(instance=obj)
        context = {'tipo': 'Sub- Setor', 'form': form}
    elif id == 7:
        if request.method == "POST":
            obj = get_object_or_404(MateriaPrima, id=pk)
            form = MateriaPrimaForm(request.POST,instance=obj)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('materiaprima_list'))
            else:
                menssagem = 'Ocorreu um erro!<br>' + str(form)
                return erro(request, menssagem)
        else:
            obj = get_object_or_404(MateriaPrima, id=pk)
            form = MateriaPrimaForm(instance=obj)
        context = {'tipo': 'Materia Prima', 'form': form}
    elif id == 8:
        if request.method == "POST":
            obj = get_object_or_404(Operador, id=pk)
            form = OperadorForm(request.POST,instance=obj)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('operador_list'))
            else:
                menssagem = 'Ocorreu um erro!<br>' + str(form)
                return erro(request, menssagem)
        else:
            obj = get_object_or_404(Operador, id=pk)
            form = OperadorForm(instance=obj)
        context = {'tipo': 'Operador', 'form': form}
    elif id == 9:
        if request.method == "POST":
            obj = get_object_or_404(Processo, id=pk)
            form = ProcessoForm(request.POST,instance=obj)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('processo_list'))
            else:
                menssagem = 'Ocorreu um erro!<br>' + str(form)
                return erro(request, menssagem)
        else:
            obj = get_object_or_404(Processo, id=pk)
            form = ProcessoForm(instance=obj)
        context = {'tipo': 'Processo', 'form': form}
    elif id == 10:
        if request.method == "POST":
            obj = get_object_or_404(POP, id=pk)
            form = PopForm(request.POST,instance=obj)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('pop_list'))
            else:
                menssagem = 'Ocorreu um erro!<br>' + str(form)
                return erro(request, menssagem)
        else:
            obj = get_object_or_404(POP, id=pk)
            form = PopForm(instance=obj)
        context = {'tipo': 'POP', 'form': form}
    elif id == 11:
        if request.method == "POST":
            user = get_object_or_404(User, id=pk)
            form =  PasswordChangeForm(user,request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('usuario_list'))
        else:
            obj = get_object_or_404(User, id=pk)
            form =  PasswordChangeForm(user=obj)
        context = {'tipo':'Alterar Senha','form':form}
    elif id == 12:
        if request.method == "POST":
            obj = get_object_or_404(FolhaObservacao, id=pk)
            form = FolhaObservacaoForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('folha_observacoes_list'))
            else:
                menssagem = 'Ocorreu um erro!<br>' + str(form)
                return erro(request, menssagem)
        else:
            obj = get_object_or_404(FolhaObservacao, id=pk)
            form = FolhaObservacaoForm(instance=obj)
        context = {'tipo': 'Alteração Folha Observação', 'form': form}

    return render(request, 'polls/forms/cadastro_form.html', context)

def exclusao_arquivo(request,id,nome):
    if id == 0:
        fs = FileSystemStorage()
        fs.delete('polls/static/polls/fluxograma/' + nome)
        return HttpResponseRedirect(reverse('fluxograma'))

def exclusao(request, id, pk,codpop):
    if id == 0:
        setor = Setor.objects.get(id=pk)
        fs = FileSystemStorage()
        fs.delete('polls/static/polls/layouts/' + setor.codigo + '.jpg')
        return HttpResponseRedirect('../../../setor_layout/' + str(setor.codigo))
    elif id == 1:
        objeto = Empresa.objects.get(id=pk)
        objeto.delete()
        return HttpResponseRedirect(reverse('empresa_list'))
    elif id == 2:
        objeto = LinhaProducao.objects.get(id=pk)
        objeto.delete()
        return HttpResponseRedirect(reverse('linhaproducao_list'))
    elif id == 3:
        objeto = Motivo_reprogramacao.objects.get(id=pk)
        objeto.delete()
        return HttpResponseRedirect(reverse('motivoreprogramacao_list'))
    elif id == 4:
        objeto = Ponto_Controle.objects.get(id=pk)
        objeto.delete()
        return HttpResponseRedirect(reverse('pontocontrole_list'))
    elif id == 5:
        objeto = Setor.objects.get(id=pk)
        objeto.delete()
        return HttpResponseRedirect(reverse('setor_list'))
    elif id == 6:
        objeto = SubSetor.objects.get(id=pk)
        objeto.delete()
        return HttpResponseRedirect(reverse('subsetor_list'))
    elif id == 7:
        objeto = MateriaPrima.objects.get(id=pk)
        objeto.delete()
        return HttpResponseRedirect(reverse('materiaprima_list'))
    elif id == 8:
        objeto = Operador.objects.get(id=pk)
        objeto.delete()
        return HttpResponseRedirect(reverse('operador_list'))
    elif id == 9:
        objeto = Processo.objects.get(id=pk)
        objeto.delete()
        return HttpResponseRedirect(reverse('processo_list'))
    elif id == 10:
        pop = POP.objects.get(id=pk)
        tarefa_list = Tarefa.objects.filter(codigo_pop=pop.codigo)
        for tarefa in tarefa_list:
            procedimento_list = Procedimento.objects.filter(codigo_tarefa=tarefa.id)
            for procedimento in procedimento_list:
                procedimento.delete()
            tarefa.delete()
        pop.delete()
        return HttpResponseRedirect(reverse('pop_list'))
    elif id == 11:
        objeto = Tarefa.objects.get(id=pk)
        list_procedimento = Procedimento.objects.filter(codigo_tarefa=pk)
        for obj in list_procedimento:
            obj.delete()
        objeto.delete()
        return HttpResponseRedirect('../../../pop_det/'+codpop)
    elif id == 12:
        objeto = Procedimento.objects.get(id=pk)
        objeto.delete()
        return HttpResponseRedirect('../../../pop_det/'+codpop)
    elif id == 13:
        user = User.objects.get(id=pk)
        if codpop == '1':
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('usuario_list'))
    elif id == 14:
        folha = FolhaObservacao.objects.get(id=pk)
        elementos = FolhaElemento.objects.filter(id_folha=folha.id)
        for elemento in elementos:
            tempos = ElementoTempo.objects.filter(id_elemento=elemento.id)
            for tempo in tempos:
                tempo.delete()
            elemento.delete()
        folha.delete()
        return HttpResponseRedirect(reverse('folha_observacoes_list'))
    elif id == 15:
        elemento = FolhaElemento.objects.get(id=pk)
        tempos = ElementoTempo.objects.filter(id_elemento=elemento.id)
        for tempo in tempos:
            tempo.delete()
        elemento.delete()
        return HttpResponseRedirect('../../../folha_observacoes/'+str(codpop)+'/1')
    else:
        return render(request, 'polls/index.html')

def exclusao_global(request, id, pk, idsec):
    if id == 1:
        object = Carteira.objects.get(id=pk)
        object.delete()
        return HttpResponseRedirect('../../../globalmanut/'+str(id)+'/'+idsec)
    elif id == 2:
        object = Devolucao.objects.get(id=pk)
        object.delete()
        return HttpResponseRedirect('../../../globalmanut/'+str(id)+'/'+idsec)
    elif id == 3:
        object = Faturamento.objects.get(id=pk)
        object.delete()
        return HttpResponseRedirect('../../../globalmanut/'+str(id)+'/'+idsec)
    elif id == 4:
        object = PrazoEntrega.objects.get(id=pk)
        object.delete()
        return HttpResponseRedirect('../../../globalmanut/'+str(id)+'/'+idsec)
    elif id == 5:
        object = Reprogramacao.objects.get(id=pk)
        object.delete()
        return HttpResponseRedirect('../../../globalmanut/'+str(id)+'/'+idsec)
    elif id == 6:
        object = ProducaoSetor.objects.get(id=pk)
        object.delete()
        return HttpResponseRedirect('../../../globalmanut/'+str(id)+'/'+idsec)

    return render(request, 'polls/index.html')

def alteracao_global(request,id,pk,idsec):
   if id == 1:
       if request.method == "POST":
           obj = get_object_or_404(Carteira, id=pk)
           form = CarteiraForm(request.POST, instance=obj)
           if form.is_valid():
               form.save()
               return HttpResponseRedirect(reverse('globalmanut', args=(id,obj.idempresa,)))
           else:
               menssagem = 'Ocorreu um erro!<br>' + str(form)
               return erro(request, menssagem)
       else:
           obj = get_object_or_404(Carteira, id=pk)
           form = CarteiraForm(instance=obj)
           empresa_list = Empresa.objects.all()
           context = {'form': form, 'empresa_list':empresa_list}
           return render(request, 'polls/forms/carteira_form.html', context)
   elif id == 2:
       if request.method == "POST":
           obj = get_object_or_404(Devolucao, id=pk)
           form = DevolucaoForm(request.POST, instance=obj)
           if form.is_valid():
               form.save()
               return HttpResponseRedirect(reverse('globalmanut', args=(id, obj.idempresa,)))
           else:
               menssagem = 'Ocorreu um erro!<br>' + str(form)
               return erro(request, menssagem)
       else:
           obj = get_object_or_404(Devolucao, id=pk)
           form = DevolucaoForm(instance=obj)
           empresa_list = Empresa.objects.all()
           context = {'form': form, 'empresa_list': empresa_list}
           return render(request, 'polls/forms/devolucao_form.html', context)
   elif id == 3:
       if request.method == "POST":
           obj = get_object_or_404(Faturamento, id=pk)
           form = FaturamentoForm(request.POST, instance=obj)
           if form.is_valid():
               form.save()
               return HttpResponseRedirect(reverse('globalmanut', args=(id, obj.idempresa,)))
           else:
               menssagem = 'Ocorreu um erro!<br>' + str(form)
               return erro(request, menssagem)
       else:
           obj = get_object_or_404(Faturamento, id=pk)
           form = FaturamentoForm(instance=obj)
           empresa_list = Empresa.objects.all()
           context = {'form': form, 'empresa_list': empresa_list}
           return render(request, 'polls/forms/faturamento_form.html', context)
   elif id == 4:
       if request.method == "POST":
           obj = get_object_or_404(PrazoEntrega, id=pk)
           form = PrazoEntregaForm(request.POST, instance=obj)
           if form.is_valid():
               form.save()
               return HttpResponseRedirect(reverse('globalmanut', args=(id,obj.linhaproducao,)))
           else:
               menssagem = 'Ocorreu um erro!<br>' + str(form)
               return erro(request, menssagem)
       else:
           obj = get_object_or_404(PrazoEntrega, id=pk)
           form = PrazoEntregaForm(instance=obj)
           empresa_list = Empresa.objects.all()
           linhaproducao_list = LinhaProducao.objects.all().order_by('descricao')
           context = {'form': form, 'empresa_list':empresa_list,'linhaproducao_list': linhaproducao_list}
           return render(request, 'polls/forms/prazoentrega_form.html', context)
   elif id == 5:
       if request.method == "POST":
           obj = get_object_or_404(Reprogramacao, id=pk)
           form = ReprogramacaoForm(request.POST, instance=obj)
           if form.is_valid():
               form.save()
               return HttpResponseRedirect(reverse('globalmanut', args=(id,obj.idsetor,)))
           else:
               menssagem = 'Ocorreu um erro!<br>' + str(form)
               return erro(request, menssagem)
       else:
           obj = get_object_or_404(Reprogramacao, id=pk)
           form = ReprogramacaoForm(instance=obj)
           empresa_list = Empresa.objects.all()
           setor_list = Setor.objects.all().order_by('nome')
           context = {'form': form, 'empresa_list':empresa_list, 'setor_list': setor_list}
           return render(request, 'polls/forms/reprogramacaoretrabalho_form.html', context)
   elif id == 6:
       if request.method == "POST":
           obj = get_object_or_404(ProducaoSetor, id=pk)
           form = ProducaoSetorForm(request.POST, instance=obj)
           if form.is_valid():
               form.update()
               return HttpResponseRedirect(reverse('globalmanut', args=(id,obj.cod_setor,)))
           else:
               menssagem = 'Ocorreu um erro!<br>' + str(form)
               return erro(request, menssagem)
       else:
           obj = get_object_or_404(ProducaoSetor, id=pk)
           form = ProducaoSetorForm(instance=obj)
           empresa_list = Empresa.objects.all()
           setor_list = Setor.objects.all().order_by('nome')
           setor = Setor.objects.get(codigo=obj.cod_setor)
           context = {'form': form, 'empresa_list':empresa_list, 'setor_list': setor_list, 'setor': setor}
           return render(request, 'polls/forms/producaosetor_form.html', context)


