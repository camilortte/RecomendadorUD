var x1,y1,x2,y2,pagina=1;
var pinColor = "47a3da";
var markers=[];
var actual_page=1;
var nombre_input,subcategoria_iput,categoria_input;
var pinImage = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + pinColor,
        new google.maps.Size(21, 34),
        new google.maps.Point(0,0),
        new google.maps.Point(10, 34));



function add_marker(lng,lat,id,nombre){
  console.log("Esto llega: "+lng+" , "+lat);
  markers.push(map.addMarker({
    lat: lat,
    lng: lng,
    icon: pinImage,
    animation: google.maps.Animation.DROP,
    id:id,
    infoWindow: {
      content: '<div style="line-height:1.35;overflow:hidden;white-space:nowrap;"><h4><a href="/establecimientos/'+id+'">'+nombre+'</h4></div>'
    },
  }));  

  console.log("markers: ");
  console.log(markers);
}


function paginador(anterior,siguiente,current){
  $('.pagination').empty();
  if(anterior){
    $('<li class="link" data-page="'+anterior+'"><a  href="#">&laquo;</a></li>').appendTo(".pagination");  
  }

  if (anterior || siguiente){
    $('<li ><a href="#">'+current+'</a></li>').appendTo(".pagination");   
  }

  if(siguiente){
    $('<li class="link" data-page="'+siguiente+'"><a  href="#">&raquo;</a></li>').appendTo(".pagination");  
  }
  

}


function send_data(){
 $.ajax({
      url: '/establecimiento/boung/',
      type: 'GET',
      data: {"x1":x1,"x2":x2,"y1":y1,
      "y2":y2,"pagina":pagina, "nombre":nombre_input,
      "categoria":categoria_input,"sub_categoria":subcategoria_iput},
      dataType: 'json',
      beforeSend: function() {  
        $( "#all_elements" ).empty();      
        $('.loading').show();   
      },
      success: function(response) {
        console.log("succes");
        console.log(response)
        console.log(response.results)

        siguiente=response.next
        anterior=response.previous
        cantidad=response.count
        console.log("Anterio")        
        paginador(anterior,siguiente,actual_page)

        map.removeMarkers();
        $( "#all_elements" ).empty();
        markers=[];
        if (response.results.length > 0){
          $("<div class='col-md-12'><h3 class='text-center'>Encontramos "+cantidad+" lugares que te gustaran</h3><br></div>").appendTo('#all_elements');
          console.log("Resultao");
          console.log(response.results);
          for (var i = response.results.length - 1; i >= 0; i--) {
            str_position=(response.results[i].position);   
            console.log(str_position);
            if (str_position){
              str_position=str_position.replace("(","");
              str_position=str_position.replace(")","");
              str_position=str_position.split(" ");

              cantidad=response.results.length
              id=response.results[i].id
              nombre=response.results[i].nombre
              subcategoria=response.results[i].sub_categorias
              descripcion=response.results[i].description
              description=""
              add_elemento(id,nombre,descripcion,subcategoria,cantidad)
              add_marker(parseFloat(str_position[1]),parseFloat(str_position[2]),id,nombre);
        }        
          };
        }  else{
            $('<div class="col-md-12"><h4 class="text-center">Opps No se encontró nada</h4></div>').appendTo("#all_elements");
        }     
        $('.loading').hide(); 
      },
      error:function(error){          
          $( "#all_elements" ).empty();
          $("<div class='col-md-12'><h3 class='text-center'>Algo salio mal</h3><br></div>").appendTo('#all_elements');
          console.log("ERROR");
          console.log(error);
      }
  });
}


//$('.link').click(function(){console.log("hola");});

$('.pagination').on('click', '.link', function(e) {
        //alert('Parameter: ' + $(this).attr('data-page').split("=")[1]);
        pagina=$(this).attr('data-page').split("=")[1];
        actual_page=$(this).attr('data-page').split("=")[1];
        send_data()

  });

function sra(){
   polygon = map.drawPolygon({
      paths: path, // pre-defined polygon shape
      strokeColor: '#BBD8E9',
      strokeOpacity: 1,
      strokeWeight: 3,
      fillColor: '#BBD8E9',
      fillOpacity: 0.6
    });

}


map = new GMaps({
  div: '#map-canvas',
  zoom: 13,
  lat: 4.579503,
  lng: -74.157113,
  scrollwheel: true,
  idle:function(e) {     
    var bounds = map.getBounds();
    var ne = bounds.getNorthEast();
    var sw = bounds.getSouthWest();
    x1=ne.lat()
    y1=sw.lng()

    x2=sw.lat()
    y2=ne.lng()

    path = [[x1,y1], [x1,y2], [x2,y2], [x2,y1],[x1,y1]];
     
    send_data(); 
  },
  mousemove: function(e){
   // console.log("Latitude: "+e.latLng.lat());
    //console.log("Longitude: "+e.latLng.lng());
  }
});


var entityMap = {    
    "<": "&lt;",
    ">": "&gt;",
    '"': '&quot;',
    "'": '&#39;',
    "/": '&#x2F;'
  };

function escapeHtml(string) {
  return String(string).replace(/[&<>"'\/]/g, function (s) {
    return entityMap[s];
  });
}


$(document).on({
    mouseenter: function () {      
      id=$(this).prop('id')
      //console.log("id");
      marker_only=$.grep(markers, function(e){ return e.id == id; })
      marker_only[0].setIcon();
    },
    mouseleave: function () {      
      id=$(this).prop('id')
      //console.log("id");
      marker_only=$.grep(markers, function(e){ return e.id == id; })
      marker_only[0].setIcon("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|47a3da");      
    }
}, ".box-info"); //pass the element as an argument to .on

function add_elemento(id,nombre,descripcion,subcategoria,cantidad){
  if (descripcion.length>100) {
      descripcion=descripcion.substring(0, 100)+"...";
  };
    
    var item= "\
    <div class='col-md-6 box-info' id='"+id+"'> \
              <a href='/establecimientos/"+id+"' >\
              <div class='media' id=''>    \
                         <div class='media-body box-est' >\
                          <br>\
                            <h4 class='media-heading text-center ' id='nombre_est'> "+escapeHtml(nombre)+" </h4>\
                            <div class='col-md-offset-1 col-md-10 col-md-offset-1'>\
                            <p class='text-justify'>"+/*descripcion*/""+"</p>\
                            <h4><small>  </small> </h4>\
                            </div> \
                        </div>     \
                </div>  \
                </a>\
                <br><br>\
            </div>  \
    "
    $(item).appendTo("#all_elements");
}

$('#boton_aplicar_filtro').click(function(){
    nombre_input=$('#filtrado').val();
    categoria_input=$('#categoria').val();
    subcategoria_iput=$('#id_sub_categorias').val();
    send_data();
});

$('#boton_limpiar').click(function(){
  console.log("limpiando");
    $('#filtrado').val(null);
    $('#categoria option[value=""]').attr("selected",true);
    $( "#categoria" ).trigger( "click" );
    nombre_input=null;
    categoria_input=null;
    subcategoria_iput=null;
    send_data();
});
