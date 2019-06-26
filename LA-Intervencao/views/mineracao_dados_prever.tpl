% rebase('layout.tpl', title='Machine Learning - Prever valores', scriptGrafico='')

<a href="/mineracao_dados?id={{idTabela}}">Voltar</a>
<div class="card">
    <div class="card-header">Prever Valores >> {{tabela.nome}} >> {{tabPrevAlg.nome}} >> {{colunaClasse}}</div>
    <div class="card-body">
        <form action="/do_mineracao_dados_prev" method="post">
            <input type="hidden" name="idTabela" value="{{idTabela}}" />
            <center>
                <input type="submit" class="btn btn-primary" value="Prever" />
            </center>
        </form>
	</div>
</div>
<br />
{{!grid}}
