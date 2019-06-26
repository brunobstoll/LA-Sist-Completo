% rebase('layout.tpl', title='Transformação - Selecionar Colunas Lookup', scriptGrafico='')

<div class="card card-register mx-auto mt-5">
    <div class="card-header">Definição Lookup</div>
    <div class="card-body">
		<form action="/do_transformacao" method="POST">
			<b>{{tabela}}</b> ( {{coluna}} ) >> <b>{{tabelaNavegacao}}</b> ( {{colunaNavegacao}} )
			<input type="hidden"  name="id_coluna" value="{{id_coluna}}" />
			<input type="hidden"  name="id_tabela" value="{{id_tabela}}" />
			<br>
			<br>
%for col in listaColunasLookup:
			<div class="checkbox">
%if col.selecionado == False:
				<label><input type="checkbox" name="coluna_{{col.id}}" value="{{col.id}}" > {{col.nome}}</label>
%else:
				<label><input type="checkbox" name="coluna_{{col.id}}" value="{{col.id}}" checked> {{col.nome}}</label>
%end
			</div>
%end
			<div class="text-center">
				<input type="submit" class="btn btn-primary" value="Aplicar" /> <a href="/transformacao?id={{id_tabela}}" class="btn btn-secondary">Voltar</a>
			</div>
		</form>
	</div>
</div>
<br>