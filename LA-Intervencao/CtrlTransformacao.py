from bottle import route, view, template, redirect, request, post, response
from datetime import datetime
import model.MetaDadosDB as meta
import model.PreProcessamentoDB as pre
import model.ImportacaoDB as imp
import controls.componentes as comp
import CtrlSeguranca as seg

# remover colunas
# usar faixas de valores

fonte_dados_transformacao = 99

@route('/transformacao')
@view('transformacao')
def Transformacao():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    return dict()

@post('/do_transformacao')
def do_transformacao():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    nome         = getattr(request.forms, 'nome')
    sql          = getattr(request.forms, 'sql')
    persistir    = getattr(request.forms, 'pers')
    descricao    = 'Gerado pela transformacao'

    nome = '__' + nome

    tabela = imp.ObterTabela('0')
    tabela.nome = nome
    tabela.descricao = descricao
    tabela.sql_origem = sql
    tabela.id_fonte_dados = fonte_dados_transformacao

    if persistir == 'N':
        tabela.sql_destino = sql
    else:
        tabela.sql_destino = None

    imp.SalvarTabela(tabela)

    if persistir == 'S':
        imp.CriarTabelaDoSql(sql, nome)
        imp.CriarIndices(nome)
        imp.GerarColunas(nome)
    else:
        imp.GerarColunasComSQL(nome, sql)

    tabela = imp.ObterTabelaPorNome(nome)

    redirect('/colunas?id=' + str(tabela.id))

