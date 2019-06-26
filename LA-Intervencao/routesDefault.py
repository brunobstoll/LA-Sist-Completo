"""
Centralizar funcionalidades comuns e import para os outros controllers

"""

from bottle import route, view
from datetime import datetime
import routesTst
import CtrlImportacao
import CtrlMetaDados
import CtrlPreProcessamento
import CtrlTransformacao
import CtrlMineracaoDados
import CtrlExplorarDados
import CtrlVisao
import CtrlUsuario
import CtrlDashboard
import CtrlSeguranca as seg
import CtrlAcessoProfessor
import CtrlAcessoAluno

@route('/')
@route('/homeAnalista')
@view('homeAnalista')
def home():
    seg.ChecarLogado()
    
    return dict(
        title='Home Page'
    )

@route('/')
@route('/homeEstudante')
@view('homeEstudante')
def homeEstudange():
    seg.ChecarPerfil(seg.PERFIL_Estudante)
    
    return dict(
        title='Home Page'
    )

@route('/')
@route('/homeProfessor')
@view('homeProfessor')
def homeEstudange():
    seg.ChecarPerfil(seg.PERFIL_Professor)
    
    return dict(
        title='Home Page'
    )

@route('/exemplo')
@view('exemplo')
def home():
    return dict(
        title='Exemplo com todos os componentes'
    )



@route('/register')
@view('register')
def login():
    return dict()