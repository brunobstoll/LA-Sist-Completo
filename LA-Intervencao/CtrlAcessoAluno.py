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
import model.VisaoDB as vis
import model.PainelDB as pnl
import model.DadosTabela as dbTab
import model.UsuarioDB as usu


@route('/recomendacao_estudante')
@route('/recomendacao_aluno')
@view('recomendacao_aluno')
def recomendacao_aluno():
    seg.ChecarPerfil(seg.PERFIL_Estudante)

    loginUsuario = seg.ObterLogin()
    usuarioLogado = usu.ObterUsuarioPorLogin(loginUsuario)

    return dm.ObterAlunosParaRecomendacoes(usuarioLogado.id)

@route('/painel_aluno_lista')
def ListaPainel():
    listaPainel = pnl.ListarPainel('A')
    lista=[]
    for painel in listaPainel:
        dpnl = dict()
        dpnl['id'] = painel.id
        dpnl['nome'] = painel.nome
        lista.append(dpnl)

    return json.dumps(lista)

@route('/painel_aluno_vw')
@view('painel_aluno_vw')
def painel_aluno_vw():
    seg.ChecarPerfil(seg.PERFIL_Estudante)

    id = request.params.get('id')
    painel = pnl.ObterPainel(id)

    # somente dados dos alunos
    if painel.tipo != 'A': 
        redirect('/homeEstudante')

    objModelo = json.loads(painel.modelo)
    ultObj = objModelo[len(objModelo) - 1]

    html = ''
    js = ''

    ultLinha = ultObj['idLinha']

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

    return dict(titulo=painel.nome,
                html=html,
                js=js)


