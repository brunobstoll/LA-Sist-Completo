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


@route('/recomendacao_professor')
@view('recomendacao_professor')
def recomendacao_professor():
    seg.ChecarPerfil(seg.PERFIL_Professor)

    id_aluno = request.params.get('id')
    if id_aluno == None:
        id_aluno = 0

    return dm.ObterAlunosParaRecomendacoes(int(id_aluno))

@post('/do_recomendacao_professor')
def do_recomendacao_professor():
    id_aluno = getattr(request.forms, 'id_aluno')

    listaRecomendacoes = dm.ObterRecomendacoesPorAluno(id_aluno)
    for msg in listaRecomendacoes:
        id_post = 'msg_' + str(msg.id)
        id_ignorarMsg = 'ignorarMsg_' + str(msg.id)

        descricao = getattr(request.forms, id_post)
        ignorarMsg = getattr(request.forms, id_ignorarMsg)

        if ignorarMsg == 'on':
            msg.descartado = 'S'
        else:
            msg.descricao = descricao

        dm.SalvarMensagem(msg)



    redirect('/recomendacao_professor')

@route('/painel_professor_lista')
def ListaPainel():
    listaPainel = pnl.ListarPainel('P')
    lista=[]
    for painel in listaPainel:
        dpnl = dict()
        dpnl['id'] = painel.id
        dpnl['nome'] = painel.nome
        lista.append(dpnl)

    return json.dumps(lista)

@route('/painel_professor_vw')
@view('painel_professor_vw')
def painel_professor_vw():
    seg.ChecarPerfil(seg.PERFIL_Professor)

    id = request.params.get('id')
    painel = pnl.ObterPainel(id)

    if painel.tipo != 'P':
        redirect('/homeProfessor')

    html = ''
    js = ''

    if painel.modelo.startswith('http') == False:
        objModelo = json.loads(painel.modelo)
        ultObj = objModelo[len(objModelo) - 1]
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
    else:
        html = '<div id="rptEmbed"></div>'
        js = '<script type="text/javascript">initViz("' + painel.modelo + '", "rptEmbed");</script>'

    return dict(titulo=painel.nome,
                html=html,
                js=js)

@route('/profAlunos')
@view('profAlunos')
def profAlunos():
    seg.ChecarPerfil(seg.PERFIL_Professor)

    colunaIdAluno = meta.ObterColunaIdAluno()
    nomeColunaClasse, idColunaClasse = meta.ObterColunaClasse(colunaIdAluno.id_tabela)

    sql = dbTab.GerarSQL(colunaIdAluno.id_tabela, 'O', [colunaIdAluno.id, idColunaClasse])
    df = dm.db.consultarSQLDataFrame(sql)

    lista = []
    for index, row in df.iterrows():
        login_aluno = row[colunaIdAluno.nome]
        usuario = usu.ObterUsuarioPorLogin(login_aluno)
        lista.append(usuario)

    campos = (  {'campo': 'login', 'titulo': 'matricula' }, {'campo': 'nome', 'titulo': 'Nome' })


    grd = comp.grid('Lista de Alunos', lista, campos)

    return dict(grid=grd)
