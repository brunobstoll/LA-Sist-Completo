from bottle import route, view, template, redirect, request, post, response
from datetime import datetime
import json
import model.MetaDadosDB as meta
import model.ImportacaoDB as imp
import controls.componentes as comp
import CtrlSeguranca as seg

@route('/colunas')
@view('md_colunas_lst')
def LstColunas():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    listaTabelas = imp.ListarTabelas()
    campos = (  {'campo': 'id_coluna_cid', 'titulo': 'ID' }, {'campo': 'comando', 'titulo': 'Nome' }, {'campo': 'tipo', 'titulo': 'Tipo'} , { 'campo': 'titulo', 'titulo': 'Titulo'}, { 'campo': 'desabilitado', 'titulo': 'Desabilitado'} )

    idTabela = request.params.get('id')
    listaColunas = meta.ListarColunas(idTabela)

    for col in listaColunas:
        col.comando = '<a href="/defcoluna?id=' + str(col.id) +  '">' + col.nome + '</a>'

    for tab in listaTabelas:
        tab.selecionado = False

    if idTabela == None:
        idTabela = 0
    else:
        for tab in listaTabelas:
            if int(tab.id) == int(idTabela):
                tab.selecionado = True

    grid = comp.grid('Lista de Colunas', listaColunas, campos , 'dados atualizados em 26/01/2018')

    return dict(listaTabelas=listaTabelas,
                grid=grid)

@route('/defcoluna')
@view('md_colunas_def')
def DefColunas():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    id = request.params.get('id')

    if id == None:
        id = 0

    coluna = meta.ObterColuna(id)
    listaTabelas = imp.ListarTabelas()
    colunasFk = None

    if coluna != None:
        if coluna.val_aluno_risco == None:
            coluna.val_aluno_risco = ''

        if coluna.chave_estrangeira == True:
            colunasFk = meta.ListarColunas(coluna.id_tabela_fk)

        coluna.lstTipos = ( { 'id': 'T', 'nome': 'Texto', 'selecionado': False }, { 'id': 'N', 'nome': 'Número', 'selecionado': False }, { 'id': 'D', 'nome': 'Data (seq. temporal)', 'selecionado': False },  )

        for tp in coluna.lstTipos:
            tp['selecionado'] = False
            if tp['id'] == coluna.tipo:
                tp['selecionado'] = True

    return dict(listaTabelas = listaTabelas, 
                colunasFk = colunasFk,
                coluna = coluna)


@post('/do_md_coluna_def')
def do_md_coluna_def():
    id                = getattr(request.forms, 'id')
    id_tabela         = getattr(request.forms, 'id_tabela')
    tipo              = getattr(request.forms, 'tipo')
    nome              = getattr(request.forms, 'nome')
    sql               = getattr(request.forms, 'sql')
    desabilitado      = getattr(request.forms, 'desabilitado') != ''
    titulo            = getattr(request.forms, 'titulo')
    descricao         = getattr(request.forms, 'descricao')
    classe            = getattr(request.forms, 'classe') != ''
    fl_aluno          = getattr(request.forms, 'fl_aluno') != ''
    chave_estrangeira = getattr(request.forms, 'chave_estrangeira') != ''
    id_tabela_fk      = getattr(request.forms, 'id_tabela_fk')
    id_coluna_fk      = getattr(request.forms, 'id_coluna_fk')
    val_aluno_risco   = getattr(request.forms, 'val_aluno_risco')
    sinonimos         = getattr(request.forms, 'sinonimos')

    coluna = meta.ObterColuna(id)
    coluna.id_tabela         = id_tabela
    coluna.tipo              = tipo
    coluna.nome              = nome
    coluna.sql               = sql
    coluna.desabilitado      = desabilitado
    coluna.titulo            = titulo
    coluna.descricao         = descricao
    coluna.classe            = classe
    coluna.fl_aluno          = fl_aluno
    coluna.chave_estrangeira = chave_estrangeira
    coluna.id_tabela_fk      = id_tabela_fk
    coluna.id_coluna_fk      = id_coluna_fk
    coluna.val_aluno_risco   = val_aluno_risco
    coluna.sinonimos   = sinonimos
    meta.SalvarColuna(coluna)

    redirect('/colunas?id=' + str(id_tabela))

@route('/tb_colunas_id')
def Obter():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    id = request.params.get('id')
    listaColunas = meta.ListarColunas(id)

    lstCol = [ ]
    for col in listaColunas:
        lstCol.append({ 'id': col.id, 'nome': col.nome })


    return json.dumps(lstCol)

