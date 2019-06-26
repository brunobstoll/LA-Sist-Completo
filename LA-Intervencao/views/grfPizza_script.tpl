<script>

// -- Pie Chart Example
var ctx = document.getElementById("{{id}}");
var myPieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: [
%for lab in labels:
		"{{lab}}",
%end
	],
    datasets: [{
      data: [
%for valor in valores:
		{{valor}},
%end

	  ],
      backgroundColor: cores,
    }],
  },
});
</script>