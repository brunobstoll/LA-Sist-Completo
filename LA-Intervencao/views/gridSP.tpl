<div class="card mb-3">
    <div class="card-header">
        <i class="fa fa-table"></i> {{titulo}}</div>
    <div class="card-body">
        <div class="table-responsive">
        <table class="table table-bordered" id="dataTableSP" width="100%" cellspacing="0">
            <thead>
				<tr>
%for col in colunas:
					<th>{{!col['titulo']}}</th>
%end
				</tr>
            </thead>
            <tfoot>
            <tr>
%for col in colunas:
					<th>{{!col['titulo']}}</th>
%end
				</tr>
            </tr>
            </tfoot>
            <tbody>
%for index, row in lista.iterrows():
				<tr>
%for col in colunas:
					<td>{{!row[ col['campo'] ]}}</td>
%end
				</tr>
%end
            </tbody>
        </table>
        </div>
    </div>
%if (informacao != ''):
	<div class="card-footer small text-muted">{{informacao}}</div>
%end
</div>
<br />
<br />
