var mapa= new GMaps({
  div: '#id_mapa',
  lat: $('#latitude').val(),
  lng: $('#longitude').val(),
    zoom: 16,
});

var myMarker = mapa.addMarker({
  lat: $('#latitude').val(),
  lng: $('#longitude').val(),
  draggable:true,
});

$('#id_position').hide();
$('#id_position').val("POINT ("+myMarker.getPosition().lng()+" "+myMarker.getPosition().lat()+")");

google.maps.event.addListener(myMarker, 'dragend', function() {
    console.log("TErminado: ");
    $('#latitude').val(myMarker.getPosition().lat());
    $('#longitude').val(myMarker.getPosition().lng());
    $('#id_position').val("POINT ("+myMarker.getPosition().lng()+" "+myMarker.getPosition().lat()+")");

     
  });

$(document).ready(function(){
 $(':input[required]:visible').each(function(){
               $(this).prev('label').after(' * ');
        });
});