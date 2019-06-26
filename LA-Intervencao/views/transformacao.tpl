% rebase('layout.tpl', title='Transformação', scriptGrafico='')

<div class="card card-register mx-auto mt-5">
		<div class="card-header">
			<i class="fa fa-table"></i> Tabelas transformadas
		</div>
        <form action="/do_transformacao" method="post">
    <div class="card-body">
		<div class="form-group row ">
			Persistir:&nbsp;&nbsp;
			<div class="radio">
				<label><input type="radio" name="pers" value="S" checked="true" > Sim *</label>
			</div>
			<div class="radio">&nbsp;&nbsp;</div>
			<div class="radio">
				<label><input type="radio" name="pers" value="N"> Não</label>
			</div>
		</div>
		<div class="form-group ">
			* O sistema indexará a tabela
		</div>
		<div class="form-group">
			<label for="nome">Nome</label>
			<input id="nome" class="form-control" name="nome" placeholder="Informe o nome da tabela" />
		</div>
		<div class="form-group">
			<label for="sql">SQL:</label>
			<textarea id="sql" name="sql" rows="3" class="form-control" placeholder="Informe o SQL. Não colocar clausula WHERE"></textarea>
		</div>
		<div class="text-center">
			<input type="submit" class="btn btn-primary" value="Salvar" /> <input type="button" value="Cancelar" onclick="window.location.href='/homeAnalista'" class="btn btn-secondary" />
		</div>
    </div>
	</form>
</div>
<br>
