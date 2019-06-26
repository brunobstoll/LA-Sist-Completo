% rebase('layout.tpl', title='Integração', scriptGrafico='')
<div class="card card-register mx-auto mt-5">
    <div class="card-header">Tabelas</div>
    <div class="card-body">
		<form method="post" action="/do_tabelas_sel">
			<input type="hidden" name="id" value="{{id}}">
			<div class="form-group">
				<div class="checkbox">
%for item in lista:
					<div class="checkbox">
						<label><input type="checkbox" name="{{item['tabela']}}" > {{item['tabela']}}</label><input type="text" class="form-control" id="nome{{item['tabela']}}" name="nome{{item['tabela']}}" value="{{item['nome']}}" >
					</div>
%end
				</div> 
			</div>
			<div class="text-center">
				<input type="submit" class="btn btn-primary btn-block" value="Salvar" />
			</div>
		</form>
	</div>
		<div class="card-footer small text-muted">Tabelas já importadas que forem desmarcadas serão eliminadas da base de dados</div>
</div>
