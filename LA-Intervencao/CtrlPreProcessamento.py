from bottle import route, view, template, redirect, request, post, response
from datetime import datetime
import model.MetaDadosDB as meta
import model.PreProcessamentoDB as pre
import model.ImportacaoDB as imp
import controls.componentes as comp
import CtrlSeguranca as seg

@route('/pre_processamento')
@view('pre_processamento')
def pre_processamento():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    listaTabelas = imp.ListarTabelas()
    idTabela = request.params.get('idTabela')
    idColuna = request.params.get('idColuna')
    nomeColuna = ''
    nomeTabela = ''
    sql=''

    for tab in listaTabelas:
        tab.selecionado = False


    if idTabela == None:
        idTabela = 0
    else:
        for tab in listaTabelas:
            if int(tab.id) == int(idTabela):
                tab.selecionado = True
                nomeTabela = tab.nome

    listaColunas = meta.ListarColunas(idTabela)
    for col in listaColunas:
        col.selecionado = False

    if idColuna == None:
        idColuna = 0
    else:
        for col in listaColunas:
            if int(col.id) == int(idColuna):
                col.selecionado = True
                nomeColuna = col.nome
                sql = col.sql

    
    resultado = None
    if idColuna != 0 and idTabela != 0:
        resultado = pre.RetornarValoresColuna(idTabela, idColuna)

    grfPizza = comp.grfPizza('Valores Válidos', resultado, 'COL', 'qtd', 'Valores válidos para a coluna selecionada');
    return dict(listaTabelas=listaTabelas, 
                listaColunas=listaColunas,
                nomeTabela=nomeTabela,
                nomeColuna=nomeColuna,
                idTabela=idTabela,
                idColuna=idColuna,
                sql=sql,
                grfPizza=grfPizza.grf,
                scriptGrafico=grfPizza.js)

@route('/gerar_sql_quartil')
def gerar_sql_quartil():
    tabela = request.params.get('tabela')
    tp     = request.params.get('tp')
    coluna = request.params.get('coluna')

    return pre.GerarSqlQuartil(tabela,coluna,tp)

@post('/do_pre_proc_discr')
def do_pre_proc_discr():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    idTabela  = getattr(request.forms, 'idTabela')
    idColuna  = getattr(request.forms, 'idColuna')
    expressao = getattr(request.forms, 'expressao')
    nome      = getattr(request.forms, 'nome')

    pre.DiscretizarCampo(idColuna, nome, expressao)

    redirect('/pre_processamento?idTabela=' + str(idTabela) + '&idColuna=' + str(idColuna))


