% rebase('layout.tpl', title='Definir Tabelas', scriptGrafico='')



<div class="card card-register mx-auto mt-5">
    <div class="card-header">Tabela</div>
    <div class="card-body">

        <form method="POST" action="/do_tabela_def">
            <input type="hidden" name="id" value="{{tabela.id}}">
           
            <div class="form-group">
                <label for="nome">Nome</label>
                <input class="form-control" name="nome" id="nome" type="text" placeholder="Informe o nome" value="{{tabela.nome}}">
            </div>
            <div class="form-group">
                <label for="descricao">Descrição</label>
                <textarea class="form-control" name="descricao" id="descricao" placeholder="Informe a descrição da tabela" rows="3">{{tabela.descricao}}</textarea>
            </div>
            <div class="form-group">
                <label for="descricao">SQL</label>
                <textarea class="form-control" name="sql_destino" id="sql_destino" placeholder="Informe o SQL - em brando indica que o sistema gerará o SQL nativamente. Não colocar clausula WHERE" rows="3">{{tabela.sql_destino}}</textarea>
            </div>
            <div class="form-group">
                <label for="descricao">SQL S/ Dados Histó"ricos</label>
                <textarea class="form-control" name="sql_sem_hist" id="sql_sem_hist" placeholder="Filtro SQL - Clausula WHERE que somente dados ativos ( sem dados históricos )" rows="3">{{tabela.sql_sem_hist}}</textarea>
            </div>
            <div class="form-group">
                <label for="pln">Permite Pln</label>
                <input type="checkbox" id="pln" name="pln" {{'checked' if (tabela.pln == "s") else "" }}
            </div>
            <div class="text-center">
                <input type="submit" class="btn btn-primary" value="Salvar" /> <input type="button" value="Cancelar" onclick="window.location.href='/lsttabelas?id={{tabela.id_fonte_dados}}'" class="btn btn-secondary" />
            </div>
        </form>
    </div>
</div>

