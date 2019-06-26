from bottle import route, view, template, redirect, request, post, response
import controls.componentes as comp
import model.UsuarioDB as usu
import CtrlSeguranca as seg


@route('/usuario')
@view('usuario_lst')
def Listar():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    campos = (  {'campo': 'id', 'titulo': 'ID' }, {'campo': 'comandoNome', 'titulo': 'Nome' }, {'campo': 'login', 'titulo': 'Login'} , { 'campo': 'ds_tipo', 'titulo': 'Tipo'} )

    lista = usu.ListarUsuario()

    grid = comp.grid('Lista de Usuários', lista, campos)

    return dict(grid=grid)


@route('/defusuario')
@view('usuario_def')
def Definir():
    seg.ChecarPerfil(seg.PERFIL_Analista)

    id = request.params.get('id')
    usuario = usu.ObterUsuario(id)

    return dict(usuario=usuario)


@post('/do_usuario_def')
def do_usuario_def():
    id    = getattr(request.forms, 'id')
    nome  = getattr(request.forms, 'nome')
    login = getattr(request.forms, 'login')
    senha = getattr(request.forms, 'senha')
    tipo  = getattr(request.forms, 'tipo')

    usuario = usu.ObterUsuario(id)
    usuario.nome = nome
    usuario.login = login
    usuario.senha = senha
    usuario.tipo = tipo

    usu.SalvarUsuario(usuario)

    redirect('/usuario')

@route('/login')
@view('login')
def login():
    seg.ClearSession()
    return dict(msg='',
                login='')

@post('/do_login')
@view('login')
def doLogin():
    login = getattr(request.forms, 'login')
    senha = getattr(request.forms, 'senha')

    valido, perfil = usu.ChecarLogin(login, senha)

    if valido == True:
        seg.Autenticar(login, perfil)
        if perfil == seg.PERFIL_Analista:
            redirect('/homeAnalista')
        elif perfil == seg.PERFIL_Estudante:
            redirect('/homeEstudante')
        elif perfil == seg.PERFIL_Professor:
            redirect('/homeProfessor')


    return dict(
        login=login,
        msg='Usuário ou senha incorretos')