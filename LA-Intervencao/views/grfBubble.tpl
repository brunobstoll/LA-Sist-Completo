<!-- Exemplo Gráfico de Área -->
<div class="card mb-3">
	<div class="card-header">
		<i class="fa fa-pie-chart"></i>{{titulo}}
	</div>
	<div class="card-body">
		<canvas id="{{id}}" width="100%" height="30"></canvas>
	</div>
%if (informacao != ''):
	<div class="card-footer small text-muted">{{!informacao}}</div>
%end
</div>
