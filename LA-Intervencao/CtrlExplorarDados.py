from bottle import route, view, template, redirect, request, post
import json
from datetime import datetime
import model.ImportacaoDB as imp
import model.MetaDadosDB as meta
import controls.componentes as comp
import model.DadosTabela as dbTab
import CtrlSeguranca as seg


@route('/explorar_dados')
@view('explorar_dados')
def explorar_dados():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    idTabela  = request.params.get('id')
    idColunas = request.params.get('idColunas')
    tipo      = request.params.get('tipo')

    listaTabelas = imp.ListarTabelas()
    listaColunas = []
    grid = ''

    if tipo == None:
        tipo = 'D'
    
    if idTabela == None:
        idTabela = 0
        idColunas = ''
        tipo = 'D'
        
    else:
        for col in meta.ListarColunas(idTabela):
            listaColunas.append(col)

        listaExibicao = dbTab.ListarExibicao(idTabela)

        for colExib in listaExibicao:
            col_lookup = meta.ObterColuna(colExib.id_coluna_fk)
            listaColunas.append(col_lookup)

        for col in listaColunas:
            col.selecionado = False

        if idColunas == None or idColunas == '':
            idColunas = ''
        else:
            splColunas = idColunas.split(',')

            for col in listaColunas:
                for idCol in splColunas:
                    if int(idCol) == int(col.id):
                        col.selecionado = True

            if len(splColunas) != 0:
                campos = meta.ListarCampos(idTabela, False, splColunas)
                if tipo == 'D':
                    resultado = dbTab.ListarDados(idTabela, splColunas)
                    grid = comp.grid('Registros', resultado, campos, '')
                elif tipo == 'I':
                    resultado = dbTab.InformDados(idTabela, splColunas)
                    #grid = comp.grid('Registros', resultado, campos, '')




    for tab in listaTabelas:
        tab.selecionado = False
        if int(tab.id) == int(idTabela):
            tab.selecionado = True

    return dict(idTabela=idTabela,
                idColunas=idColunas,
                tipo=tipo,
                listaTabelas=listaTabelas,
                listaColunas=listaColunas,
                grid=grid)

@post('/do_explorar_dados')
def do_explorar_dados():
    idTabela = getattr(request.forms, 'idTabela')
    colunas  = getattr(request.forms, 'colunas')
    tipo     = getattr(request.forms, 'tipo')

    redirect('/explorar_dados?id=' + str(idTabela) + '&idColunas=' + colunas + '&tipo=' + tipo)