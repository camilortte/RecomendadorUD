$(document).ready(function() {
    //
    $(".fancybox").fancybox({
        openEffect  : 'none',
        closeEffect : 'none'
    });
    map = new GMaps({
      div: '#map-canvas',
      zoom: 16,
      lat: ($('#latitude').val()),
      lng: ($('#longitude').val()),
      scrollwheel: false
    });
    map.addMarker({
      lat: ($('#latitude').val()),
      lng: ($('#longitude').val())
    });
});


$("#rating").rating({
    max:5,
    showClear: false,
    clearCaption: "Sin Calificar",
    starCaptions:{
        1:"Muy bajo",
        2:"Bajo",
        3:"Medio",
        4:"Bueno",
        5:"Excelente"
    }            
});    

$("#rating_general").rating({
    clearCaption: "Sin Calificar",
    starCaptions:{
        1:"Muy bajo",
        2:"Bajo",
        3:"Medio",
        4:"Bueno",
        5:"Excelente"
    }            
});  

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

 
//Modificar mensage modal error
function modal(msg,title){
    $('#generic_modal_title').text(title);
    $('#generic_modal_body').text(msg);        
}


//Cuando se califica se envia la informacion
$('#rating').on('rating.change', function(event, value, caption) {
    $.ajax({
        url: "/establecimiento/calificar/"+$("#id").val()+"/",
        type: 'POST',  
        data: {"calificacion":value},        
        dataType: 'json',           
        complete: function(xhr) {                   
            if (xhr.readyState == 4) {
                if (xhr.status == 201) {
                    console.log("ENVIADO "+xhr);
                    recibirdata();
                }
            }
        },
        error:function(error){
            console.log("ERROR ");
            alert("Error: "+error);
            //location.reload();
        },
        beforeSend: function(xhr, settings) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(data) {
            modal("Gracias por su calificación","Calificación realizada","Calificación realizada");
            $('#generic_modal').modal('show');
        }
    });
    console.log(value);
    console.log(caption);
    //$('#rating').rating('update', 3);
});

function recibirdata(){
        $.ajax({
            url: "/establecimiento/calificar/"+$("#id").val()+"/",
            type: 'GET',                      
            dataType: 'json',
            success: function( data, status ){     
                var rating_usuario=data.rating_usuario
                console.log(data)
                var ratin_estableicimiento =data.ratin_estableicimiento 
                if  (rating_usuario ){
                    $('#rating').rating('update',data.rating_usuario );
                }
                if(ratin_estableicimiento){
                    $('#rating_general').rating('update',data.ratin_estableicimiento );
                }
            },
            error:function(error){
                console.log("ERROR ");
                console.log(error);
                //location.reload();
            },
            beforeSend: function(xhr, settings) {
                  xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
    });
 }

recibirdata();

$('.add_comment_submit').click(function() {
    $.ajax({
        url: $('#my_form').attr('action'),
        type: 'POST',
        data: $('#my_form').serialize(),                
        dataType: 'json',
        success: function(response) {
            if(response.success){
                location.reload();
            } else {
                $('.form-error').remove();
                for(var error in response.errors.fields) {
                    $('#my_form #id_' + error).before('<div class="form-error">' + response.errors.fields[error] + '</div>');
                }
            }
        },
        error:function(error){
            console.log("ERROR");
        }
    });
});


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

//Modificar mensage modal error
function set_error_modal_message(error){
    $('#modal_body_error_message').text(error);
}



$('#fileupload').fileupload({
    url: "/establecimientos/"+$("#id").val()+"/upload2/",
    type: 'POST',
    dataType: 'json',
    beforeSend: function(xhr, settings) {
               xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    disableImageResize: /Android(?!.*Chrome)|Opera/
        .test(window.navigator.userAgent),
    maxFileSize: 5000000,
    acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,    
    add: function (e, data) {
        var goUpload = true;
        var uploadFile = data.files[0];
        if (!(/\.(jpg|jpeg|png)$/i).test(uploadFile.name)) {
            //common.notifyError('You must select an image file only');
            set_error_modal_message('Solo se aceptan imagenes con la extención .jpg .jpeg .png');
            $('#modal_error_upload').modal('show');
            goUpload = false;
        }else{
            if (uploadFile.size > 10485760) { // 2mb
                set_error_modal_message('La imagen supera los 10MB.');
                $('#modal_error_upload').modal('show');
                goUpload = false;
            }else{
                if (goUpload == true) {
                    data.submit();
                }   
            }
        }
    },
    progressall: function (e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        $('#progress .progress-bar').css(
            'width',
            progress + '%'
        );
    },
    success: function(data) {        
        $('#modal_upload_ok').modal('show');
    },
    error: function(data){
            console.log("error");
            console.log(data.responseJSON.error);
            error=data.responseJSON.error
            set_error_modal_message((error).toString());
            $('#modal_error_upload').modal('show');
            $('#progress .progress-bar').css(
                'width',
                0 + '%'
            );
    }
});



//Recargar la pagina cuando acepten el modal dialog
$('#ok_upload').click(function(){
    location.reload();
})
