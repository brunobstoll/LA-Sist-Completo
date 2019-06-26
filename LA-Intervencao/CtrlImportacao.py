from bottle import route, view, template, redirect, request, post
import json
from datetime import datetime
import model.ImportacaoDB as imp
import controls.componentes as comp
import CtrlSeguranca as seg
import os

@route('/importacao')
@view('importacao_source')
def Importacao():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    lista = imp.ListarFontes()

    campos = {'campo': 'nome_edt', 'titulo': 'Nome' }, {'campo': 'descr_tipo', 'titulo': 'Tipo'} , { 'campo': 'comando_tabelas', 'titulo': 'Tabelas'}

    grid = comp.grid('Lista de Fontes de Dados', lista, campos, 'dados atualizados em 26/01/2018')

    return dict(grid = grid)

@route('/importacao_id')
def Obter():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    id = request.params.get('id')
    obj = imp.ObterFonte(id)

    return json.dumps({
        'id': obj.id,
        'nome': obj.nome,
        'tipo': obj.tipo,
        'valor': obj.valor
        })


@post('/do_importacao')
def Do_Importacao():

    id      = getattr(request.forms, 'id')
    tipo    = getattr(request.forms, 'tipo')
    nome    = getattr(request.forms, 'nome')
    valor   = getattr(request.forms, 'valor')
    arquivo = request.files.get('arquivo')

    fileName, ext = os.path.splitext(arquivo.filename)
    if tipo == 'C' and ext != '.csv':
        return 'Arquivo inválido <br><a href="#" onclick="window.history.go(-1)">Voltar</a>'
    if tipo == 'J' and ext != '.csv':
        return 'Arquivo inválido <br><a href="#" onclick="window.history.go(-1)">Voltar</a>'

    if arquivo != None:
        path = "/home/bstoll/mysite/arquivosUpld"
        #path = "C:\Users\bstoll\source\repos\LA-Intervencao\LA-Intervencao\LA-Intervencao.pyproj\arquivosUpld"
        path_save = "{path}/{file}".format(path=path, file=arquivo.filename)

        if os.path.isfile(path_save):
            os.remove(path_save)

        arquivo.save(path_save)
        valor = path_save

    obj = imp.ObterFonte(id)
    obj.tipo = tipo
    obj.nome = nome
    obj.valor = valor
    imp.SalvarFonte(obj)

    redirect('/importacao')

@route('/tabelas')
@view('importacao_tabelas_lst')
def ImpTabelasTst():
    return dict()

@route('/seltabelas')
@view('importacao_tabelas_sel')
def SelTabelas():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    id = request.params.get('id')

    lista = imp.ListarTabelasFonte(id)

    return dict(lista = lista, id = id)


@post('/do_tabelas_sel')
def Do_Tabelas_Sel():
    formulario = request.forms

    id = formulario.get('id')

    lista = imp.ListarTabelasFonte(id)

    for tb in lista:
        tabela = tb['tabela']
        if formulario.get( tabela ) == None:
            imp.RemoverTabela(tabela)
        else:
            imp.ExecutarImportacao(id)

    redirect('/importacao')


@route('/deftabelas')
@view('importacao_tabelas_def')
def DefTabelas():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    return dict()

@route('/lsttabelas')
@view('importacao_tabelas_lst')
def ListTabelas():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    id = request.params.get('id')

    lista = imp.ListarTabelas(id)

    campos = ({'campo': 'id', 'titulo': 'Id' }, {'campo': 'comandoNome', 'titulo': 'Nome' })


    grid = comp.grid('Lista de Tabelas', lista, campos)

    return dict(grid=grid)


@route('/edttabela')
@view('importacao_tabelas_edt')
def edtTabela():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    id = request.params.get('id')

    tabela = imp.ObterTabela(id)

    if tabela.descricao == None:
        tabela.descricao = ''
    if tabela.sql_destino == None:
        tabela.sql_destino = ''

    return dict(tabela=tabela)

@post('/do_tabela_def')
def do_tabela_def():

    id           = getattr(request.forms, 'id')
    descricao    = getattr(request.forms, 'descricao')
    sql_destino  = getattr(request.forms, 'sql_destino')
    sql_sem_hist = getattr(request.forms, 'sql_sem_hist')
    pln          = getattr(request.forms, 'pln')

    tabela = imp.ObterTabela(id)

    tabela.descricao    = descricao
    tabela.sql_destino  = sql_destino
    tabela.sql_sem_hist = sql_sem_hist
    tabela.pln          = "s" if pln == 'on' else "n"

    imp.SalvarTabela(tabela)

    redirect('/importacao')

@route('/indexarTab')
def indexarTab():
    nome = request.params.get('nome')

    imp.CriarIndices(nome)

    return 'Índices (re)criados!'
