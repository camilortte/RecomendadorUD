
$('#categoria').click(function() {

        console.log("categoria clic");
        // using jQuery
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            var csrftoken = getCookie('csrftoken');

        $.ajax({
            url: '/api2/sub_categoria/?categoria='+$('#categoria').val()+"&?format=json",     
            type: 'GET',
            dataType: 'json',
            success: function(response) {   
                $('#id_sub_categorias').empty().append('<option value="" >----Todas----</option>');
                for (var i = response.length - 1; i >= 0; i--) {
                    console.log(response[i].tag);
                    $('#id_sub_categorias').append('<option value="'+response[i].id+'">'+response[i].tag +'</option>');
                };
                console.log("\n");
            },
            error:function(){
                console.log("ERROR");
                //location.reload();
            },
            beforeSend: function(xhr, settings) {
                  xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        });


});



