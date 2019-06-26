% rebase('layout.tpl', title='Colunas', listaTabelas)

<div class="card card-register mx-auto mt-5">
    <div class="card-header">Colunas</div>
    <div class="card-body">
		<form>
			<div class="form-group">
				<label for="nome">Tabela</label>
				<select class="form-control">
					<option>1</option>
					<option>2</option>
					<option>3</option>
					<option>4</option>
				</select>
			</div>
			<div class="form-group">
				<label for="nome">Nome</label>
				<input class="form-control" name="nome" id="nome" type="text" placeholder="Informe o nome">
			</div>
			<div class="checkbox">
				<label><input type="checkbox"> Desabilitar</label>
			</div>
			
			<div class="form-group">
				<label for="nome">T�tulo</label>
				<input class="form-control" name="nome" id="nome" type="text" placeholder="Informe o T�tulo">
			</div>
			<div class="form-group">
				<label for="nome">Descri��o</label>
				<textarea class="form-control" name="nome" id="nome" placeholder="Informe a descri��o do campo" rows="3">
				</textarea>
			</div>
			<div class="checkbox">
				<label><input type="checkbox"> Classe ( na predi��o - valores n�los ser�o previstos )</label>
			</div>
			<div class="checkbox">
				<label><input type="checkbox"> Identifica��o Aluno</label>
			</div>
			<div class="checkbox">
				<label><input type="checkbox"> Chave Estrangeira</label>
			</div>
			<div class="form-group">
				<label for="nome">Tabela</label>
				<select class="form-control">
					<option>1</option>
					<option>2</option>
					<option>3</option>
					<option>4</option>
				</select>
			</div>
			<div class="form-group">
				<label for="nome">Coluna</label>
				<select class="form-control">
					<option>1</option>
					<option>2</option>
					<option>3</option>
					<option>4</option>
				</select>
			</div>
		</form>
		<div class="text-center">
			<input type="submit" class="btn btn-primary btn-block" value="Salvar" />
		</div>
	</div>
</div>
