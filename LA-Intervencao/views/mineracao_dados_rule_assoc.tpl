% rebase('layout.tpl', title='Machine Learning - Regras de Associção', scriptGrafico=jsTree)

<a href="/mineracao_dados?id={{tabela.id}}">Voltar</a>
<div class="card card-register mx-auto mt-5">
    <div class="card-header">Regras de Associação</div>
    <div class="card-body">
        <div class="form-group">
            <label for="tamTst">Tabela</label>
            <input class="form-control" value="{{tabela.nome}}" readonly>
        </div>
        {{!treeView}}
	</div>
</div>
