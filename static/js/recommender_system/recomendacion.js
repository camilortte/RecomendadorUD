

	$( document ).ready(function() {
		if ($(window).width() >= 900){	
			console.log("Mayor (Y)");
			// do something here
			var heights = $(".recomendacion").map(function() {
		        return $(this).height();
		    }).get();   
		    maxHeight = Math.max.apply(null, heights);
		    $(".recomendacion").height(maxHeight);
		}	else {
			console.log("Menor");
		}		  
	});

	



lista=$( ".contenedir" ).children()
for (var i = lista.length - 1; i >= 0; i--) {	
	imagen=$(lista[i]).find(".recomendacion-img")
	id=imagen.attr("id")

	$(lista[i]).find(".recomendacion-img").attr("id")
	latitude=$(lista[i]).find("#latitude_"+id).val()
	longitude=$(lista[i]).find("#longitude_"+id).val()

	console.log("Latitude:"+latitude)
	console.log("Longitude; "+longitude)

	url = GMaps.staticMapURL({
	  size: [250,450],
	  lat: latitude,	
	  lng: longitude,
	  markers: [
	    {lat: latitude, lng:longitude,
	      color: 'blue'}
	  ],
	  zoom:16
	});

	imagen.attr('src', url)

	// imagen_background=$(lista[i]).find("#imagen_"+id).val();
	// console.log("Esto es imagen_background");
	// console.log(imagen_background);
	// $('#lugar_'+id).css("background-image", "url("+imagen_background+")");  

};
