<script>

var dadosTree{{id}} = [
%for item in lista:
    {
        text: '{{item[campoTexto]}}',
        tags: ['{{item[campoValor]}}'],
        href: '#',
        nodes: [
%for filho in item[campoFilhos]:
        {
            text: '{{filho[campoTexto]}}',
            href: '#',
            tags: ['{{filho[campoValor]}}']
        },
%end
        ]
    },
%end
    ];

$('#{{id}}').treeview({
    levels: 999,
    showTags: true,
    data: dadosTree{{id}}
});


</script>