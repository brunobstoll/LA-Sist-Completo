<div class="card o-hidden h-100 ">
    <div class="card-header"><i class="fa fa-newspaper-o"></i> {{!titulo}}</div>
    <div class="card-body">
        <div class="mr-5"></div>
        <div class="small card-footer">
%for item in lista:
%for col in colunas:
            <label><b>{{!item[col]}}</b></label>
%end
            <br />
%end
        </div>
    </div>
</div>

