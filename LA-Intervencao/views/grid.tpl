<div class="card mb-3">
    <div class="card-header">
        <i class="fa fa-table"></i> {{titulo}}</div>
    <div class="card-body">
        <div class="table-responsive">
        <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
            <thead>
				<tr>
%for col in colunas:
					<th>{{col['titulo']}}</th>
%end
				</tr>
            </thead>
            <tfoot>
            <tr>
%for col in colunas:
					<th>{{col['titulo']}}</th>
%end
				</tr>
            </tr>
            </tfoot>
            <tbody>
%for item in lista:
				<tr>
%for col in colunas:
%if type(item) is dict:
                    <td>{{!item[col['campo']]}}</td>
%else:
					<td>{{!getattr(item,col['campo'])}}</td>
%end
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
