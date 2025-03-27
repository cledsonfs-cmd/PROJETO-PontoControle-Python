from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.telalogin, name='login'),
    path('sair/', views.sair, name='sair'),
    path('carteira/', views.carteira, name='carteira'),
    path('devolucao/', views.devolucao, name='devolucao'),
    path('faturamento/', views.faturamento, name='faturamento'),
    path('prazoentrega/', views.prazoentrega, name='prazoentrega'),
    path('producaogeral/', views.producaogeral, name='producaogeral'),
    path('reprogramacaoretrabalho/', views.reprogramacaoretrabalho, name='reprogramacaoretrabalho'),
    path('erro/', views.erro, name='erro'),
    path('admin/', views.admin, name='admin'),
    path('pop_list/', views.pop_list, name='pop_list'),
    path('pop_det/<int:id>', views.pop_det, name='pop_det'),
    path('pop_view/<int:id>', views.pop_view, name='pop_view'),
    path('empresa_list/', views.empresa_list, name='empresa_list'),
    path('linhaproducao_list/', views.linhaproducao_list, name='linhaproducao_list'),
    path('motivoreprogramacao_list/', views.motivoreprogramacao_list, name='motivoreprogramacao_list'),
    path('pontocontrole_list/', views.pontocontrole_list, name='pontocontrole_list'),
    path('setor_list/', views.setor_list, name='setor_list'),
    path('subsetor_list/', views.subsetor_list, name='subsetor_list'),
    path('materiaprima_list/', views.materiaprima_list, name='materiaprima_list'),
    path('operador_list/', views.operador_list, name='operador_list'),
    path('processo_list/', views.processo_list, name='processo_list'),
    path('setor/<str:id>/', views.setor, name='setor'),
    path('evento_pc/<str:id>/', views.evento_pc, name='evento_pc'),
    path('globalmanut/<str:id>/<str:idsec>/', views.globalmanut, name='globalmanut'),
    path('setor_layout/<str:codigo>/', views.setor_layout, name='setor_layout'),
    path('usuario_list/', views.usuario_list, name='usuario_list'),

    # Histórico
    path('carteira_his/<str:ano>/<str:mes>/', views.carteira_his, name='carteira_his'),
    path('devolucao_his/<str:ano>/<str:mes>/', views.devolucao_his, name='devolucao_his'),
    path('faturamento_his/<str:ano>/<str:mes>/', views.faturamento_his, name='faturamento_his'),
    path('prazoentrega_his/<str:ano>/<str:mes>/', views.prazoentrega_his, name='prazoentrega_his'),
    path('producaogeral_his/<str:ano>/<str:mes>/', views.producaogeral_his, name='producaogeral_his'),
    path('reprogramacao_his/<str:ano>/<str:mes>/', views.reprogramacao_his, name='reprogramacao_his'),
    path('setor_his/<str:id>/<str:ano>/<str:mes>/', views.setor_his, name='setor_his'),

    # Formulários
    path('carteira_form/', views.carteira_form, name='carteira_form'),
    path('devolucao_form/', views.devolucao_form, name='devolucao_form'),
    path('faturamento_form/', views.faturamento_form, name='faturamento_form'),
    path('prazoentrega_form/', views.prazoentrega_form, name='prazoentrega_form'),
    path('reprogramacaoretrabalho_form/', views.reprogramacaoretrabalho_form, name='reprogramacaoretrabalho_form'),
    path('producaosetor_form/<str:id>/', views.producaosetor_form, name='producaosetor_form'),
    path('cadastros_form/<int:id>/<str:codigo>/', views.cadastros_form, name='cadastros_form'),
    path('evento_pc_form/<int:id>/', views.evento_pc_form, name='evento_pc_form'),
    path('exclusao/<int:id>/<int:pk>/<str:codpop>', views.exclusao, name='exclusao'),
    path('alteracao/<int:id>/<int:pk>', views.alteracao, name='alteracao'),
    path('exclusao_global/<int:id>/<int:pk>/<str:idsec>', views.exclusao_global, name='exclusao_global'),
    path('alteracao_global/<int:id>/<int:pk>/<str:idsec>', views.alteracao_global, name='alteracao_global'),
    path('layout_form/<str:codigo>', views.layout_form, name='layout_form'),
    path('fluxograma_form/', views.fluxograma_form, name='fluxograma_form'),
    path('imgpop_form/<int:id>/<int:idsec>', views.imgpop_form, name='imgpop_form'),

    # Ferramentas
    path('matrizbcg/', views.matrizbcg, name='matrizbcg'),
    path('fluxograma/', views.fluxograma, name='fluxograma'),
    path('folha_observacoes_list/', views.folha_observacoes_list, name='folha_observacoes_list'),
    path('folha_observacoes/<int:id>/<int:alt>', views.folha_observacoes, name='folha_observacoes'),
    path('exclusao_arquivo/<int:id>/<str:nome>', views.exclusao_arquivo, name='exclusao_arquivo'),

    # Relatórios
    path('devolucao_rel/<int:id>/<str:ano>/', views.devolucao_rel, name='devolucao_rel'),
]
