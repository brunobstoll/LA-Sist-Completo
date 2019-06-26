from bottle import route, view, template, redirect, request, post
import json
from datetime import datetime
import model.ImportacaoDB as imp
import model.MetaDadosDB as meta
import controls.componentes as comp
import model.DadosTabela as dbTab
import model.VisaoDB as vis
import model.PainelDB as pnl
import model.DadosTabela as dbTab
import CtrlSeguranca as seg


@route('/dashboard')
@view('dashboard_lst')
def Listar():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    campos = ( {'campo': 'id', 'titulo': 'id' },  {'campo': 'comandoEditar', 'titulo': 'Nome' },  {'campo': 'ds_tipo', 'titulo': 'Tipo'} ,  {'campo': 'comandoVisualizar', 'titulo': 'Visualizar'}  )

    lista = pnl.ListarPainel()

    grid = comp.grid('Lista de Paineis', lista, campos, 'dados atualizados em 26/01/2018')
    return dict(grid=grid)

@route('/defdashboard')
@view('dashboard_def')
def dashboard_def():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    id = request.params.get('id')

    painel = pnl.ObterPainel(id)

    painel.ds_tipo = { }
    painel.ds_tipo['P'] = ''
    painel.ds_tipo['A'] = ''

    if painel.tipo == 'P':
        painel.ds_tipo['P'] = 'checked'
    elif painel.tipo == 'A':
        painel.ds_tipo['A'] = 'checked'

    listaVisao = vis.ListarVisao(0)

    return dict(listaVisao=listaVisao,
                painel=painel,
                js='<script>ReconstruirGrid();</script>')


@post('/do_painel')
def do_painel():
    id = getattr(request.forms,'id')
    nome = getattr(request.forms,'nome')
    tipo = getattr(request.forms,'tipo')
    modelo = getattr(request.forms,'modelo')

    painel = pnl.ObterPainel(id)
    painel.nome = nome
    painel.tipo = tipo
    painel.modelo = modelo

    pnl.SalvarPainel(painel)

    redirect('/dashboard')

@route('/viewdashboard')
@view('dashboard_vw')
def viewdashboar():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    id = request.params.get('id')
    painel = pnl.ObterPainel(id)

    if painel.modelo.startswith('http') == False:
        objModelo = json.loads(painel.modelo)
        if len(objModelo) == 0:
            redirect('/dashboard')

        ultObj = objModelo[len(objModelo) - 1]

        html = ''
        js = ''

        ultLinha = int(ultObj['idLinha'])

        for linha in range(1, ultLinha + 1):
            htmlLinha = '<div id="row' + str(linha) + '" class="row">'

            for i in range(0, len(objModelo)):
                corrObjModelo = objModelo[i]

                if corrObjModelo['idLinha'] == linha:
                    id_visao = corrObjModelo['id_visao']

                    objGrf = comp.defGrafico('', '')
                    if id_visao != 0:
                        objGrf = dbTab.GerarVisao(id_visao)

                    htmlCell = '<div class="col-lg-' + corrObjModelo['opcaoColuna'] + '">' + objGrf.grf + '</div>'
                    htmlLinha = htmlLinha + htmlCell
                    js = js + objGrf.js

            htmlLinha = htmlLinha + '</div><br>'
            html = html + htmlLinha
    else:
        html = '<div id="rptEmbed"></div>'
        js = '<script type="text/javascript">initViz("' + painel.modelo + '", "rptEmbed");</script>'

    return dict(titulo=painel.nome,
                    html=html,
                    js=js)

@route('/viewdashboardpln')
@view('dashboard_pln_vw')
def PlnPainel():
    expressao = seg.GetSession('expressao')
    html = ''
    js = ''

    if expressao == None:
        expressao = ''

    if expressao != '':
        html, js = pnl.PainelDinamicoPln(expressao)
    
    seg.SetSession('expressao', '')
    

    return dict(titulo='Pergunte aos seus dados',
                expressao=expressao,
                js=js,
                html=html)

@post('/do_dashboard_pln')
def do_PlnPainel():
    expressao = getattr(request.forms,'expressao')
    seg.SetSession('expressao', expressao)

    redirect('/viewdashboardpln')






