import bottle as app
import bottle_session
from bottle import route, view, post, request, redirect, template

from datetime import datetime
import model.dataBase as db
#from beaker.middleware import SessionMiddleware
import CtrlSeguranca as seg


PERFIL_Estudante = 'E'
PERFIL_Professor = 'P'
PERFIL_Analista  = 'A'

def GetSession(key):
    app_session = request.environ.get('beaker.session')
    try:
        return app_session[key]
    except (KeyError, TypeError):
        return None

def ClearSession():
    SetSession('logado', False)
    SetSession('usuario', '')
    SetSession('perfil', '')

    app_session = request.environ.get('beaker.session')
    app_session.clear()
    app_session.save()

def SetSession(key, value):
    app_session = request.environ.get('beaker.session')
    app_session[key] = value

    app_session.save()

def ChecarLogado():
    if not GetSession('logado') == True:
        redirect('/login')

def ChecarPerfil(perfilUsuario):
    ChecarLogado()

    if not GetSession('perfil') == perfilUsuario:
        redirect('/login')

def Autenticar(pUsuario, pPerfil):
    SetSession('logado', True)
    SetSession('usuario', pUsuario)
    SetSession('perfil', pPerfil)

def ObterLogin():
    return GetSession('usuario')
