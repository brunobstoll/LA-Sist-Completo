import model.dataBase as db

def ListarUsuario():
    session = db.getSession()
    lista = session.query(db.Usuario).all()
    session.close()

    for usuario in lista:
        usuario.comandoNome = '<a href="/defusuario?id=' + str(usuario.id) + '">' + usuario.nome + '</a>'
        if usuario.tipo == 'P':
            usuario.ds_tipo = 'Professor'
        elif usuario.tipo == 'E':
            usuario.ds_tipo = 'Estudante'
        elif usuario.tipo == 'A':
            usuario.ds_tipo = 'Analista'        

    return lista


def SalvarUsuario(usuario):
    session = db.getSession()

    if int(usuario.id) == 0:
        usuario.id = None
        session.add(usuario)
    else:
        iid = usuario.id
        obj2 = session.query(db.Usuario).filter_by(id=iid).first()
        obj2.nome = usuario.nome
        obj2.login = usuario.login
        obj2.senha = usuario.senha
        obj2.tipo = usuario.tipo

    session.commit()
    session.close()

def ObterUsuario(iid):
    usuario = None
    if int(iid) == 0:
        usuario = db.Usuario(0,'','','','A')
    else:
        session = db.getSession()
        usuario = session.query(db.Usuario).filter_by(id=iid).first()
        session.close()

    usuario.ds_tipo = {  }
    usuario.ds_tipo['A'] = ''
    usuario.ds_tipo['P'] = ''
    usuario.ds_tipo['E'] = ''

    if usuario.tipo == 'A':
        usuario.ds_tipo['A'] = 'selected'
    elif usuario.tipo == 'P':
        usuario.ds_tipo['P'] = 'selected'
    elif usuario.tipo == 'E':
        usuario.ds_tipo['E'] = 'selected'

    return usuario

def ChecarLogin(llogin, ssenha):
    session = db.getSession()

    usuario = session.query(db.Usuario).filter_by(login=llogin).filter_by(senha=ssenha).first()

    if usuario == None:
        return False, ''
    else:
        return True, usuario.tipo

    session.close()

def ObterUsuarioPorLogin(llogin):
    session = db.getSession()
    usuario = session.query(db.Usuario).filter_by(login=llogin).first()
    session.close()

    return usuario