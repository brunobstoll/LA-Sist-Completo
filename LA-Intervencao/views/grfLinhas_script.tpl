<script>
var ctx = document.getElementById("{{id}}");
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
        labels: [
%for categ in valoresCateg:
        "{{categ}}",
%end
        ],
    datasets: [
%for idx_serie in range(0, len(valoresSeries)):
    {
      label: "{{valoresSeries[idx_serie]}}",
      fill: false,
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
    ],
  },
});

</script>
