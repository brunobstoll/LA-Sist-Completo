% rebase('layout.tpl', title='Machine Learning - Cluster', scriptGrafico=jsGrf)

<a href="/mineracao_dados?id={{tabela.id}}">Voltar</a>
<div class="card">
    <div class="card-header">Agrupamento ( Cluster )</div>
    <div class="card-body">
        <div class="form-group">
            <label for="tamTst">Tabela</label>
            <input class="form-control" value="{{tabela.nome}}" readonly>
        </div>
        <div class="form-group">
				<label>Cluster</label>
			</div>
			<div class="form-group row ">
%for disp in display:
				<div class="radio form-group">
					&nbsp;&nbsp;<label><input type="radio" name="tipo" value="C"> <input class="form-controlx" type="text" value="{{disp}}" /></label>
				</div>
%end            
			</div>
        

        {{!htmlGrf}}

	</div>
</div>
