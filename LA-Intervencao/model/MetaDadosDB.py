import model.dataBase as db


def ListarColunas(iid_tabela):
    session = db.getSession()
    lista = session.query(db.Coluna).filter_by(id_tabela=iid_tabela).all()
    session.close()

    return lista

def ListarColunasPorTipo(iid_tabela, ttipo):
    session = db.getSession()
    lista = session.query(db.Coluna).filter_by(id_tabela=iid_tabela).filter_by(tipo=ttipo).all()
    session.close()

    return lista

def ObterColuna(iid):

    if int(iid) ==  0:
        return db.Coluna(iid, 100, 0, '', '', 'T', '', '', False, False, False, False, None, None, None, None)
    else:
        session = db.getSession()
        obj = session.query(db.Coluna).filter_by(id=iid).first()
        session.close()
        return obj

def SalvarColuna(coluna):
    session = db.getSession()

    if int(coluna.id) == 0:
        coluna.id = None
        session.add(coluna)
    else:
        iid = coluna.id
        obj2 = session.query(db.Coluna).filter_by(id=iid).first()
        obj2.id_coluna_cid = coluna.id_coluna_cid
        obj2.id_tabela = coluna.id_tabela
        obj2.nome = coluna.nome
        obj2.sql = coluna.sql
        obj2.tipo = coluna.tipo
        obj2.titulo = coluna.titulo
        obj2.descricao = coluna.descricao
        obj2.desabilitado = coluna.desabilitado
        obj2.classe = coluna.classe
        obj2.fl_aluno = coluna.fl_aluno
        obj2.chave_estrangeira = coluna.chave_estrangeira
        obj2.id_tabela_fk = coluna.id_tabela_fk
        obj2.id_coluna_fk = coluna.id_coluna_fk
        obj2.val_aluno_risco = coluna.val_aluno_risco
        obj2.sinonimos = coluna.sinonimos

    session.commit()
    session.close()

def ObterColunaPorTabNome(idTabela, nome):
    session = db.getSession()
    obj = session.query(db.Coluna).filter_by(id_tabela=idTabela).filter_by(nome=nome).first()
    session.close()

    return obj

def ObterColunaClasse(idTabela=None):
    session = db.getSession()
    if idTabela != None:
        obj = session.query(db.Coluna).filter_by(id_tabela=idTabela).filter_by(classe=True).first()
    else:
        obj = session.query(db.Coluna).filter_by(classe=True).first()

    session.close()
    if obj != None:
        return obj.nome, obj.id

    return '', None

def ObterColunaIdAluno(idTabela=None):
    session = db.getSession()
    if idTabela != None:
        obj = session.query(db.Coluna).filter_by(id_tabela=idTabela).filter_by(fl_aluno=True).first()
    else:
        obj = session.query(db.Coluna).filter_by(fl_aluno=True).first()

    session.close()

    return obj

def ListarCampos(idTabela, edt = True, splColunas = []):
    listaCampos = ListarColunas(idTabela)

    campos = [ ]

    for col in listaCampos:
        #if col.desabilitado == True:
        #    continue

        if len(splColunas) != 0:
            existeColunaFiltro = False
            for idCol in splColunas:
                if int(idCol) == int(col.id):
                    existeColunaFiltro = True

            if existeColunaFiltro == False:
                continue


        if col.chave_estrangeira == False or edt == False:
            c_campo = {'campo': col.nome, 'titulo': col.titulo }
        else:
            c_campo = {'campo': col.nome, 'titulo': '<a href="transformacao_sel?idTabela=' + str(idTabela) + '&idColuna=' + str(col.id) + '">' + col.titulo + '</a>' }

        campos.append(c_campo)    

    return campos