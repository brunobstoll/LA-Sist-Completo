from bottle import route, view, template, redirect, request, post, response
from datetime import datetime
import model.ImportacaoDB as imp
import model.MetaDadosDB as meta
import model.MineracaoDadosDB as dm
import ml.descritivo as descr
import controls.componentes as comp
import json
from operator import itemgetter
import CtrlSeguranca as seg

# remover colunas
# usar faixas de valores

@route('/mineracao_dados')
@view('mineracao_dados')
def mineracao_dados():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    idTabela = request.params.get('id')

    tam_tst = 15

    id_coluna = 0
    colunaClasse = ''

    if idTabela == None:
        idTabela = 0

    listaTabelas = imp.ListarTabelas()
    tabPred = None
    listaTabelaDesc = []
    listaColunaT = []
    listaColunaN = []

    if int(idTabela) != 0:
        colunaClasse, id_coluna = meta.ObterColunaClasse(idTabela)
        tabPred = dm.ObterTabelaPredicao(idTabela)
        listaTabelaDesc = dm.ListarTabelaDescricao(idTabela)

        listaColunaT = meta.ListarColunasPorTipo(idTabela, 'T')
        listaColunaN = meta.ListarColunasPorTipo(idTabela, 'N')

        if tabPred != None:
            tam_tst = tabPred.reserva_treino


    for tab in listaTabelas:
        tab.selecionado = False
        if int(tab.id) == int(idTabela):
            tab.selecionado = True

    return dict(idTabela=idTabela,
                tam_tst=tam_tst,
                listaTabelas=listaTabelas,
                id_coluna=id_coluna,
                colunaClasse=colunaClasse,
                tabPred=tabPred,
                listaTabelaDesc=listaTabelaDesc,
                listaColunaT=listaColunaT,
                listaColunaN=listaColunaN)

@post('/do_mineracao_dados_predict')
def do_mineracao_dados_predict():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    id_tabela    = getattr(request.forms, 'id_tabela')
    id_coluna    = getattr(request.forms, 'id_coluna')
    tam_tst      = getattr(request.forms, 'tamTst')
    
    modelo = dm.CalcularPreditivo(id_tabela, id_coluna, int(tam_tst))

    redirect('/mineracao_dados?id=' + id_tabela)

@route('/mineracao_dados_executar_tudo')
def mineracao_dados_executar_tudo():
    id_tabela = request.params.get('id')
    id_coluna = meta.ObterColunaClasse(id_tabela)[1]

    tam_tst = 20
    dm.CalcularPreditivo(id_tabela, id_coluna, int(tam_tst))
    dm.GerarRecomendacoes(id_tabela)

    redirect('/mineracao_dados?id=' + str(id_tabela))

@post('/do_mineracao_dados_descrit')
def do_mineracao_dados_descrit():

    filtro        = getattr(request.forms, 'filtro')
    id_tabela     = getattr(request.forms, 'id_tabela')
    association   = getattr(request.forms, 'association') != None
    n_association = getattr(request.forms, 'n_association')

    cluster       = getattr(request.forms, 'cluster') != None
    n_cluster     = getattr(request.forms, 'n_cluster')

    outlier       = getattr(request.forms, 'outlier') != None
    d_outlier     = getattr(request.forms, 'd_outlier')
    v_outlier     = getattr(request.forms, 'v_outlier')

    pattern_seq   = getattr(request.forms, 'pattern_seq') != None
    summarization = getattr(request.forms, 'summarization') != None

    if cluster == True:
        dm.Cluster(id_tabela, filtro, n_cluster)

    if association == True:
        dm.Association(id_tabela, filtro, n_association)

    if outlier == True:
        dm.Outlier(id_tabela, filtro, d_outlier, v_outlier)

    redirect('/mineracao_dados?id=' + id_tabela)

@route('/mineracao_dados_predict')
@view('mineracao_dados_predict')
def mineracao_dados_predict():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    idModPredAlg = request.params.get('id')
    idTabela = request.params.get('idTabela')

    return dm.ExibirMatrizConfusao(idTabela, idModPredAlg)

@route('/mineracao_dados_pesos')
@view('mineracao_dados_pesos')
def mineracao_dados_pesos():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    idModPredAlg = request.params.get('id')

    return dm.ExibirPesos(idModPredAlg)

@route('/mineracao_dados_treeview')
@view('exemploTreeView')
def mineracao_treeview():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    idTabela = request.params.get('id')

    lista = dm.ListarDadosTOP10(idTabela)
    regras = descr.Association(lista, 100)

    objTree = comp.treeView(regras, 'campos', 'lift', 'Regras')

    return dict(treeView=objTree.grf,
                jsTree=objTree.js)

@route('/mineracao_dados_cluster')
@view('mineracao_dados_cluster')
def mineracao_dados_cluster():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    idTabela = request.params.get('idTabela')
    id       = request.params.get('id')

    tabela = imp.ObterTabela(idTabela)
    tabDesc = dm.ObterTabelaDescr(id)
    #objModelo = {
    #    'n_clusters': qtd_clusters,
    #    'modeloDados': modeloDados,
    #    'clusters': clusters.tolist(),
    #    'labels' : labels.tolist()
    #    }

    modelo = json.loads(tabDesc.modelo)
    n_clusters = modelo['n_clusters']
    modeloDados = modelo['modeloDados']
    clusters = modelo['clusters']
    labels = modelo['labels']
    display = modelo['display']

    lista = []
    for itemCluster in clusters:
        valores2 = []
        for valor in itemCluster:
            valores2.append(int(round(valor, 3)))

        lista.append(valores2)

    grf = comp.grfBolha('Clusters', lista, labels, '')



    return dict(tabela=tabela,
                display=display,
                htmlGrf=grf.grf,
                jsGrf=grf.js)

@route('/mineracao_dados_rule_assoc')
@view('mineracao_dados_rule_assoc')
def mineracao_dados_rule_assoc():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    idTabela = request.params.get('idTabela')
    id       = request.params.get('id')

    tabela = imp.ObterTabela(idTabela)
    tabDesc = dm.ObterTabelaDescr(id)
    regras = json.loads(tabDesc.modelo)
    regrasOrdenadas = sorted(regras, key=itemgetter('lift'), reverse=True)


    objTree = comp.treeView(regrasOrdenadas, 'campos', 'lift', 'Regras')

    return dict(tabela=tabela,
                treeView=objTree.grf,
                jsTree=objTree.js)

@route('/mineracao_dados_outlier')
@view('mineracao_dados_outlier')
def mineracao_dados_outlier():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    idTabela = request.params.get('idTabela')
    id       = request.params.get('id')

    tabela = imp.ObterTabela(idTabela)
    tabDesc = dm.ObterTabelaDescr(id)

    modelo = json.loads(tabDesc.modelo)

    grfOutlier = comp.grfOutliers(modelo['lista'], modelo['campoD'], modelo['campoV'])

    return dict(tabela=tabela,
                htmlGrf=grfOutlier.grf,
                jsGrf=grfOutlier.js)

@route('/mineracao_dados_prever')
@view('mineracao_dados_prever')
def mineracao_dados_prever():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    idTabela = request.params.get('id')

    tabela = imp.ObterTabela(idTabela)
    tabPrev = dm.ObterTabelaPredicao(idTabela)
    tabPrevAlg = None
    colunaClasse, id_coluna = meta.ObterColunaClasse(idTabela)

    tabelaPrev = dm.ObterDadosPrevisao(idTabela)
    colunas = []
    for col in tabelaPrev.columns:
        if col == "rowid":
            continue

        coluna = meta.ObterColunaPorTabNome(idTabela, col)
        
        colunas.append( {'campo': coluna.nome, 'titulo': coluna.titulo } ) 

    grid = comp.gridSP('Modelo DB para previsão', tabelaPrev, colunas, '')


    for alg in tabPrev.Alg:
        if alg.selecionado:
            tabPrevAlg = alg

    return dict(idTabela=idTabela,
                tabela=tabela,
                tabPrev=tabPrev,
                tabPrevAlg=tabPrevAlg,
                colunaClasse=colunaClasse,
                grid=grid)

@post('/do_mineracao_dados_prev')
def do_mineracao_dados_prev():
    idTabela = getattr(request.forms, 'idTabela')

    dm.PreverValores(idTabela)

    redirect('/mineracao_dados_prever?id=' + idTabela)

@route('/mineracao_dados_recomendar')
@view('mineracao_dados_recomendar')
def mineracao_dados_recomendar():
    idTabela = request.params.get('id')
    gerarMsg = request.params.get('gerar')

    if gerarMsg == 'S':
        dm.GerarRecomendacoes(idTabela)

    return dm.ListarRecomendacoes(idTabela)

    


    

