% rebase('layout.tpl', title='Machine Learning - Predição', scriptGrafico='')

<a href="/mineracao_dados?id={{idTabela}}">Voltar</a>
<div class="card card-register mx-auto mt-5">
    <div class="card-header">Definicao</div>
    <div class="card-body">
		<div class="form-group">
			<label for="tabela">Tabela</label>
			<input class="form-control" name="tabela" type="text" readonly value="{{tabela}}" />
		</div>
		<div class="form-group">
			<label for="colunaClasse">Coluna Classe</label>
			<input class="form-control" name="colunaClasse" type="text" readonly value="{{colunaClasse}}" />
		</div>
		<div class="form-group">
			<label for="dt_processo">Data de Precessamento</label>
			<input class="form-control" name="dt_processo" type="text" readonly value="{{dt_processo}}" />
		</div>
		<div class="form-group">
			<label for="algoritmo">Algoritmo</label>
			<input class="form-control" name="algoritmo" type="text" readonly value="{{algoritmo}}" />
		</div>
	</div>
</div>
<br>
<table border="1" style="width: 100%">
<tr>
	<td>&nbsp;</td>
%for valorClf in valoresCls:
	<td><b>{{valoresCls[valorClf]}}</b></td>
%end
</tr>
%for valorClfX in valoresCls:
<tr>
	<td><b>{{valoresCls[valorClfX]}}</b></td>
%for valorClfY in valoresCls:
	<td>{{matriz_confusao[int(valorClfX)][int(valorClfY)]}}</td>
%end
</tr>
%end
</table>
<br>
<br>