import model.dataBase as db
import model.MetaDadosDB as meta
import model.ImportacaoDB as imp

def RetornarTipo(id_tipo):
    tipo = {  }
    tipo['1']  = 'Gráfico de Pizza'
    tipo['2']  = 'Gráfico Barras'
    tipo['3']  = 'Gráfico Linha'
    tipo['4']  = 'Informação em Cards'
    tipo['5']  = 'Informação em Grid'

    if id_tipo in tipo:
        return tipo[id_tipo]
    else:
        return ''

def ListarVisao(idTabela):
    session = db.getSession()
    if idTabela == 0:
        lista = session.query(db.Visao).all()
    else:
        lista = session.query(db.Visao).filter_by(id_tabela=idTabela).all()

    session.close()

    for vis in lista:
        vis.ds_tipo = RetornarTipo(vis.tipo)
        vis.visualizarCommando = '<a href="/exibirvisao?id=' + str(vis.id) + '">Exibir</a>'
        vis.nomeCommando = '<a href="/defvisao?id_tabela=' + str(vis.id_tabela) + '&id=' + str(vis.id) + '">' + vis.nome + '</a>'

    return lista

def ObterVisao(iid):
    session = db.getSession()
    if int(iid) != 0:
        obj = session.query(db.Visao).filter_by(id=iid).first()
    else:
        obj = db.Visao(int(iid))
    
    session.close()

    return obj

def SalvarVisao(visao):
    session = db.getSession()

    if int(visao.id) == 0:
        visao.id = None
        session.add(visao)
    else:
        iid = visao.id
        obj2 = session.query(db.Visao).filter_by(id=iid).first()
        obj2.id_tabela = visao.id_tabela
        obj2.nome = visao.nome
        obj2.tipo = visao.tipo
        obj2.modelo = visao.modelo

    session.commit()
    session.close()

