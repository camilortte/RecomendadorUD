
var jQuery = django.jQuery;

$(function () {
  $('#categoria').click(function() {
            var data = JSON.stringify({
                "categorias": $('#categoria').val()
            });

            $.ajax({
                url: '/api/SubCategoriaResource/?categorias='+$('#categoria').val(),
                type: 'GET',
                data: data,
                dataType: 'json',
                success: function(response) {   
                    console.log(response);
                    $('#id_sub_categorias').empty().append('-------');
                    console.log("CATEGORIA: "+$('#categoria').val());
                    for (var i = response.length - 1; i >= 0; i--) {
                        console.log(response[i].tag);
                         $('#id_sub_categorias').append('<option value="'+response[i].id+'">'+response[i].tag +'</option>');
                    };
                    console.log("\n");
                },
                error:function(){
                    console.log("ERROR");
                    //location.reload();
                }
            });


        });
});



