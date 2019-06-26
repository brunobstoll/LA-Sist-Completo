// Call the dataTables jQuery plugin
$(document).ready(function() {
    $('#dataTable').DataTable();
    

    $('#dataTableSP').DataTable({
        "bPaginate": false,
        "scrollX": false
    });
});
