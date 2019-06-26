from bottle import route, view, template, redirect, request, post, response
from datetime import datetime
import model.MetaDadosDB as meta
import model.PreProcessamentoDB as pre
import model.ImportacaoDB as imp
import model.TransformacaoDB as tranf
import controls.componentes as comp
import CtrlSeguranca as seg

# remover colunas
# usar faixas de valores

@route('/reprocessar')
@view('reprocessar')
def Transformacao():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    return dict()

@post('/do_reprocessar')
def reprocessar():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    


