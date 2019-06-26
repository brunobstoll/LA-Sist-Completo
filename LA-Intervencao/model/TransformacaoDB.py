import model.dataBase as db
import model.MetaDadosDB as meta
import model.ImportacaoDB as imp
import model.DadosTabela as dbTab



def GerarSQLTop10(idTabela):
    return dbTab.GerarSQL(idTabela) + ' LIMIT 10'

def ListarDadosTOP10(idTabela):    
    sql = GerarSQLTop10(idTabela)
    resultado = db.consultarSQL(sql)

    return resultado


def ObterTotalRegistros(idTabela):
    tabela = imp.ObterTabela(idTabela)
    sql_table = tabela.nome
    if not (tabela.sql_destino == None or tabela.sql_destino == ''):
        sql_table = tabela.sql_destino

    sql = 'SELECT COUNT(*) AS qtd FROM ' + sql_table
    resultado = db.consultarSQL(sql)

    return resultado[0]['qtd']

def ListarCampos(idTabela, edt = True, splColunas = []):
    listaCampos = meta.ListarColunas(idTabela)
    listaExibicao = dbTab.ListarExibicao(idTabela)

    campos = [ ]

    for col in listaCampos:
        if col.desabilitado == True:
            continue

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

    conta_tb = 0
    for colExib in listaExibicao:

        col = meta.ObterColuna(colExib.id_coluna_fk)
        if col.desabilitado == True:
            continue

        if len(splColunas) != 0:
            existeColunaFiltro = False
            for idCol in splColunas:
                if int(idCol) == int(col.id):
                    existeColunaFiltro = True

            if existeColunaFiltro == False:
                continue

        conta_tb = conta_tb + 1

        if edt == True:
            c_campo = {'campo': col.nome, 'titulo': '<a href="#" style="color: red;">' + col.titulo + '</a>' }
        else:
            c_campo = {'campo': col.nome, 'titulo': col.titulo }


        campos.append(c_campo)

    return campos

def ObterColunaClasse(idTabela):
    session = db.getSession()
    obj = session.query(db.Coluna).filter_by(id_tabela=idTabela).filter_by(classe=True).first()
    session.close()
    if obj != None:
        return obj.nome, obj.id       
    else:
        listaExibicao = dbTab.ListarExibicao(idTabela)

        for colExib in listaExibicao:
            col = meta.ObterColuna(colExib.id_coluna_fk)

            if col.classe:
                return col.nome, col.id

    return '', None



def RemoverColExibicao(idTabela, idColuna, idColunaLookup):
    session = db.getSession()
    obj = session.query(db.ExibicaoColuna).filter_by(id_tabela=idTabela).filter_by(id_coluna=idColuna).filter_by(id_coluna_fk=idColunaLookup).first()

    if obj != None:
        session.delete(obj)
        session.commit()

    session.close()

def AdicionarColExibicao(id_tabela, id_coluna, id_col_sel_lookup):
    session = db.getSession()

    colunaLookup = session.query(db.Coluna).filter_by(id=id_col_sel_lookup).first()

    obj = session.query(db.ExibicaoColuna).filter_by(id_tabela=id_tabela).filter_by(id_coluna_fk=id_col_sel_lookup).first()

    if obj == None:
        obj = db.ExibicaoColuna(None, id_tabela, id_coluna, colunaLookup.id_tabela, id_col_sel_lookup)
        session.add(obj)
        session.commit()

    session.close()


