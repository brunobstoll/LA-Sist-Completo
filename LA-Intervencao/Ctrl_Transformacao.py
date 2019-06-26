from bottle import route, view, template
from datetime import datetime


@route('/importacao')
@view('imp_source')
def Importacao():
    arq = ""
    return dict()

@route('/tabelas')
@view('imp_tabelas')
def Tabelas():
    arq = ""
    return dict()

@route('/lstColunas')
@view('imp_colunas_lst')
def ListarColunas():
    arq = ""
    return dict()


@route('/colunas')
@view('imp_colunas')
def Colunas():
    arq = ""
    return dict()
