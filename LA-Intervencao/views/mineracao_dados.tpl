% rebase('layout.tpl', title='Machine Learning', scriptGrafico='')

<div class="card mb-3">
    <!-- <i class="fa fa-table"></i> Data Table Example</div> -->
    <div class="card-body">
        <div class="form-group">
            <label for="nome">Tabela</label>
            <select id="id" class="form-control" onchange="sel(this)">
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
    </div>
</div>

%if idTabela != 0:
<div class="row">
	<div class="col-lg-4">
		<div class="card card-register mx-auto mb-3"><!--mt-5-->
			<div class="card-header">
                <i class="fa fa-flask"></i> Parâmetros para predição
            </div>
			<div class="card-body">
				<form action="/do_mineracao_dados_predict" method="POST">
					<input type="hidden" name="id_tabela" id="id_tabela" value="{{idTabela}}" />
%if colunaClasse != '':
					<div class="form-group">
						<input type="hidden" name="id_coluna" id="id_coluna" value="{{id_coluna}}" />
						<label for="colunaClasse">Classe ( valores núlos serão previstos )</label>
						<input class="form-control" name="colunaClasse" type="text" readonly value="{{colunaClasse}}">
					</div>
					<div class="form-group">
						<label for="tamTst">Reservar para testes (%)</label>
						<input class="form-control" name="tamTst" id="tamTst" type="number" min="0" step="1" value="{{tam_tst}}">
					</div>

%if tabPred != None:
                    <div class="form-group">
                        <label for="dt_processamento">Dt. Processamento</label>
                        <input class="form-control" name="dt_processo" type="text" readonly value="{{tabPred.dt_processo}}">
                    </div>
%end
					<div class="text-center">
						<input type="submit" class="btn btn-primary btn-block" value="Aplicar" />
					</div>
%end
				</form>


			</div>
		</div>
	</div>
    <div class="col-lg-8">
        <div class="card card-register mx-auto mb-3 ">
            <div class="card-header">
                <i class="fa fa-search"></i> Resultado
            </div>
            <div class="card-body">
%if tabPred != None:
                <div class="form-group">
                    <input type="button" class="btn " value="Prever valores" onclick="window.location.href='/mineracao_dados_prever?id={{tabPred.id_tabela}}'" />
                    <input type="button" class="btn " value="Visualizar Pesos" onclick="window.location.href='/mineracao_dados_pesos?id={{tabPred.id_tabela}}&gerar=N'" />
                    
                    <input type="button" class="btn " value="Listar Recomen" onclick="window.location.href='/mineracao_dados_recomendar?id={{tabPred.id_tabela}}&gerar=N'" />
                    <input type="button" class="btn " value="Gerar Recomen" onclick="window.location.href='/mineracao_dados_recomendar?id={{tabPred.id_tabela}}&gerar=S'" />
                </div>
                    <table class="table-bordered" style="width: 99%; border: solid 1px #CCC;">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Algoritmo</th>
                                <!--<th>Pontos</th>-->
                                <th style="text-align: right;">Acur</th>
                                <th style="text-align: right;">Sen</th>
                                <th style="text-align: right;">Esp</th>
                                <th style="text-align: right;">Efic</th>
                                <th style="text-align: right;">VPP</th>
                                <!--<th style="text-align: right;">TotP</th>-->
                                <th style="text-align: right;">VPN</th>
                                <!--<th style="text-align: right;">TotN</th>-->
                            </tr>
                        </thead>
                        <tbody>
%for alg in tabPred.Alg:
%if alg.selecionado:
                            <tr style="font-weight: bold;">
                                <td>*</td>
%else:
                            <tr>
                                <td>&nbsp;</td>
%end
                                <td><a href="/mineracao_dados_predict?idTabela={{idTabela}}&id={{alg.id}}">{{alg.nome}}</a></td>
                                <!--<td>{{alg.pontos}}</td>-->
                                <!--<td style="text-align: right;">{{alg.tx_acerto}}</td>-->
                                <td style="text-align: right;">{{alg.calcular(alg.matriz_confusao, 'acur')}}</td>
                                <td style="text-align: right;">{{alg.calcular(alg.matriz_confusao, 'sens')}}</td>
                                <td style="text-align: right;">{{alg.calcular(alg.matriz_confusao, 'esp')}}</td>
                                <td style="text-align: right;">{{alg.calcular(alg.matriz_confusao, 'efic')}}</td>
                                <td style="text-align: right;">{{alg.calcular(alg.matriz_confusao, 'VPP')}}</td>
                                <!--<td style="text-align: right;">{{alg.calcular(alg.matriz_confusao, 'totP')}}</td>-->
                                <td style="text-align: right;">{{alg.calcular(alg.matriz_confusao, 'VPN')}}</td>
                                <!--<td style="text-align: right;">{{alg.calcular(alg.matriz_confusao, 'totN')}}</td>-->
                            </tr>
%end
                        </tbody>
                    </table>
                    <span style="font-size: 8pt">* Algoritmo selecionado para prever os registros com a classe vazia
                        <br />
                        <b>Acur</b>: Acurácia<br />
                        <b>Sens</b>: Sensibilidade<br />
                        <b>Esp</b>: Especificidade<br />
                        <b>Efic</b>: Eficiência<br />
                        <b>VPP</b>: Valor Preditivo Positivo<br />
                        <b>VPN</b>: Valor Preditivo Negativo
                </span>
%end
                </div>
        </div>
    </div>
<!--
	<div class="col-lg-6">
		<div class="card card-register mx-auto mb-3 ">
			<div class="card-header">Descritivo</div>
			<form action="/do_mineracao_dados_descrit" method="POST">
				<input type="hidden" name="id_tabela" value="{{idTabela}}" />
				<div class="card-body">
                    <div class="form-group row">
                        <div class="radio">
                            &nbsp;&nbsp;<label><input type="radio" name="filtro" value="T" checked> Tudo&nbsp;&nbsp;</label>
                        </div>
                        <div class="radio">
                            <label><input type="radio" name="filtro" value="H"> Dados históricos&nbsp;&nbsp;</label>
                        </div>
                        <div class="radio">
                            <label><input type="radio" name="filtro" value="A"> Dados ativos</label>
                        </div>
                    </div>
                    <hr />
					<div class="checkbox">
						<label><input type="checkbox" name="association" onclick="Descr(this)"> Associação</label><input id="n_association" name="n_association" type="number" class="form-control" placeholder="Top Regras (expl.: 15)" disabled value="100" />
					</div>
                    <hr />
					<div class="checkbox">
						<label><input type="checkbox" name="cluster" onclick="Descr(this)"> Agrupamento ( <i>Cluster</i> )</label><input id="n_cluster" name="n_cluster" type="number" class="form-control" placeholder="Num clusters" disabled value="4" />
					</div>
                    <hr />
					<div class="checkbox">
						<label><input type="checkbox" name="outlier" onclick="Descr(this)"> Detecção de desvios ( <i>Outliers</i> )</label>
                        <br />
                        Descrição:
                        <select class="form-control" name="d_outlier" id="d_outlier" disabled>
%for col in listaColunaT:
                            <option value="{{col.id}}">{{col.titulo}}</option>
%end
                        </select>
                        Valores:
                        <select class="form-control" name="v_outlier" id="v_outlier" disabled>
%for col in listaColunaN:
                            <option value="{{col.id}}">{{col.titulo}}</option>
%end
                        </select>
					</div>
                    <hr />
					<div class="checkbox">
						<label><input type="checkbox" name="pattern_seq" disabled> <strike>Padrães Sequenciais</strike></label>
					</div>
					<div class="checkbox">
						<label><input type="checkbox" name="summarization" disabled> <strike>Sumarização</strike></label>
					</div>
					<div class="text-center">
						<input type="submit" class="btn btn-primary btn-block" value="Gerar" />
					</div>
				</div>
			</form>

%if len(listaTabelaDesc) > 0:
            <br>
            <table class="table-bordered" style="width: 99%">
                <thead>
                    <tr>
                        <th>Algoritmo</th>
                        <th>Dt. Processo</th>
                    </tr>
                </thead>
                <tbody>
%for alg in listaTabelaDesc:
                    <tr>
                        <td><a href="{{alg.link}}">{{alg.des_alg}}</a></td>
                        <td>{{alg.dt_processo}}</td>
                    </tr>
%end
                </tbody>
            </table>
%end
		</div>
	</div>
-->
</div>

%end
<script>
function sel() {
    var id = $('#id').val();
    window.location.href = '/mineracao_dados?id=' + id;
}

function Descr(obj) {
    var n_obj = 'n_' + obj.name;
    var d_obj = 'd_' + obj.name;
    var v_obj = 'v_' + obj.name;

    if (!obj.checked) {
        $("#" + n_obj).prop('disabled', true);
        $("#" + d_obj).prop('disabled', true);
        $("#" + v_obj).prop('disabled', true);
    } else {
        $("#" + n_obj).prop('disabled', false);
        $("#" + d_obj).prop('disabled', false);
        $("#" + v_obj).prop('disabled', false);
    }
}
</script>