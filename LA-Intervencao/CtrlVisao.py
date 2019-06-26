from bottle import route, view, template, redirect, request, post, response
from datetime import datetime
import model.MetaDadosDB as meta
import model.PreProcessamentoDB as pre
import model.ImportacaoDB as imp
import model.VisaoDB as vis
import controls.componentes as comp
import model.DadosTabela as dbTab
import CtrlSeguranca as seg

from datetime import datetime
import json


@route('/visao')
@view('visao_lst')
def visao():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    id_tabela = request.params.get('id')
    if id_tabela == None or id_tabela == '':
        id_tabela = 0

    listaTabelas = imp.ListarTabelas()

    for tab in listaTabelas:
        tab.selecionado = False
        if int(tab.id) == int(id_tabela):
            tab.selecionado = True


    lista = vis.ListarVisao(id_tabela)

    campos = (  {'campo': 'id', 'titulo': 'ID' }, {'campo': 'nomeCommando', 'titulo': 'Nome' },{'campo': 'visualizarCommando', 'titulo': 'Mostrar' }, {'campo': 'ds_tipo', 'titulo': 'Tipo'} )

    grid = comp.grid('Lista de Visões', lista, campos)


    return dict(listaTabelas=listaTabelas,
                grid=grid)

@route('/defvisao')
@view('visao_def')
def def_visao():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    id_tabela = request.params.get('id_tabela')
    id = request.params.get('id')
    nome = ''
    modelo = ''
    tipo = {  }
    tipo['1']  = ''
    tipo['2']  = ''
    tipo['3']  = ''
    tipo['4']  = ''
    tipo['5']  = ''

    tabela = imp.ObterTabela(id_tabela)
    listaColunas = meta.ListarColunas(id_tabela)
    for col in listaColunas:
        col.selecionado = False

    visao = None
    if id != '0':
        visao = vis.ObterVisao(id)
        nome = visao.nome
        dTipo = visao.tipo
        modelo = visao.modelo

        tipo[dTipo] = 'selected'

        objModelo = json.loads(modelo)

        for col in listaColunas:
            for mod in objModelo:
                if int(mod['id_coluna']) == col.id:
                    col.selecionado = True

    else:
        tipo['1'] = 'checked'

    return dict(id=id,
                nome=nome,
                tipo=tipo,
                modelo=modelo,
                idTabela=id_tabela,
                nomeTabela=tabela.nome,
                listaColunas=listaColunas,
                visao=visao,
                js='<script>ReconstruirGrid();</script>')

@post('/do_visao_def')
def do_visao_def():
    id        = getattr(request.forms, 'id')
    id_tabela = getattr(request.forms, 'id_tabela')
    nome      = getattr(request.forms, 'nome')
    tipo      = getattr(request.forms, 'tipo')
    modelo    = getattr(request.forms, 'modelo')

    visao = vis.ObterVisao(id)
    visao.id_tabela = id_tabela
    visao.nome = nome
    visao.tipo = tipo
    visao.modelo = modelo

    vis.SalvarVisao(visao)

    redirect('/visao?id='+id_tabela)

@route('/exibirvisao')
@view('visao_exibir')
def visao_exibir():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    idVisao = request.params.get('id')
    visao = vis.ObterVisao(idVisao)
    objGrf = dbTab.GerarVisao(idVisao)


    return dict(idTabela=visao.id_tabela,
                html=objGrf.grf,
                js=objGrf.js)






