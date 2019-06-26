<script>
var ctx = document.getElementById("{{id}}");
var myLineChart = new Chart(ctx, {
  type: 'bar',
  data: {
        labels: [
%for categ in valoresCateg:
        "{{categ}}",
%end
        ],
    datasets: [
%if len(valoresSeries) == 0:
		{
		  label: "Unica",
		  backgroundColor: cores[{{0}}],
		  borderColor: cores[{{0}}],
		  data: [
	%for categ in valoresCateg:
		%if len(lista[campoValor][(lista[campoCateg] == categ)].values) > 0:
					{{lista[campoValor][(lista[campoCateg] == categ)].values[0]}},
		%else:
					0,
		%end 
				
	%end
		],
	}
%else:
	%for idx_serie in range(0, len(valoresSeries)):
		{
		  label: "{{valoresSeries[idx_serie]}}",
		  backgroundColor: cores[{{idx_serie}}],
		  borderColor: cores[{{idx_serie}}],
		  data: [
	%for categ in valoresCateg:
	%if len(lista[campoValor][(lista[campoCateg] == categ) & (lista[campoSerie] == valoresSeries[idx_serie])].values) > 0:
				{{lista[campoValor][(lista[campoCateg] == categ) & (lista[campoSerie] == valoresSeries[idx_serie])].values[0]}},
	%else:
				0,
	%end      
	%end
		  ],
		},
	%end
%end
    ],
  },
});
</script>
