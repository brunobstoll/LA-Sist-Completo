<script>

    var ctx = document.getElementById("{{id}}");
var myLineChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [
%for item in lista:
        "{{item[campoD]}}",
%end
        ],
        datasets: [
            {
                label: "{{campoV}}",
                fill: false,
                backgroundColor: cores[9],
                data: [
%for item in lista:
                {{item[campoV]}},
%end
                ],
            },
            {
                label: "Média",
                fill: false,
                backgroundColor: cores[1],
                data: [
%for item in lista:
                {{item['media']}},
%end
                ],
            },
            {
                label: "lSup",
                fill: false,
                backgroundColor: cores[2],
                data: [
%for item in lista:
                {{item['lSup']}},
%end
                ],
            },
            {
                label: "lInf",
                fill: false,
                backgroundColor: cores[3],
                data: [
%for item in lista:
                {{item['lInf']}},
%end
                ],
            },
            ],
    },
});
</script>
