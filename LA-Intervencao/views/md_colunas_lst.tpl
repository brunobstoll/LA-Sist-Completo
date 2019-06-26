% rebase('layout.tpl', title='Colunas', listaTabelas=listaTabelas, scriptGrafico='')

<div class="card card-register mx-auto mt-5">
    <div class="card-header">Filtro</div>
    <div class="card-body">
		<div class="form-group">
			<label for="nome">Tabela</label>
			<select id="id" name="id" class="form-control" onchange="sel(this)">
				<option value="0">Selecione uma tabela</option>
%for tab in listaTabelas:
%if tab.selecionado == True:
				<option value="{{tab.id}}" selected>{{tab.nome}}</option>
%else:
				<option value="{{tab.id}}">{{tab.nome}}</option>
%end
%end
			</select>
		</div>
		<div class="text-center">
			<input type="button" value="Adicionar" onclick="window.location.href='/defcoluna?id=0'" class="btn" />
		</div>
	</div>
</div>
<br>
<script>

function sel(sel) {
id = $('#id').val()
window.location.href = '/colunas?id=' + id
}

</script>
{{!grid}}


