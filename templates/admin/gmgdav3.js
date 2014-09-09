{% extends "gis/admin/openlayers.js" %}
{% block base_layer %}new OpenLayers.Layer.Google("Google Hybrid", {type: google.maps.MapTypeId.ROADMAP});{% endblock %}

{% block controls %}
{{ block.super }}

django.jQuery(document).ready(function() {
	
	var mappa = {{ module }}.map;
	var lng, lat
	var $address = django.jQuery('#id_address');
	
	$address.change(function() {
		geocod($address.val(), mappa);
	});
	
	django.jQuery('#id_longitude, #id_latitude').change(function() {
		lng = django.jQuery("#id_longitude").val();
		lat = django.jQuery("#id_latitude").val();
		modcoo(lng, lat, mappa);
		revgeocod(lng, lat, mappa); 
	});
	
	django.jQuery('[id*="OpenLayers.Layer.Vector_39_"]').click(function() { 
		srco = document.getElementById('{{ id }}').value;
		var a = srco.split(" ");
		var b = a[0].split("(");
		var c = a[1].split(")");
		lngm = parseFloat(c[0]);
		latm = parseFloat(b[1]);
		var c = new OpenLayers.Geometry.Point(latm,lngm).transform(new OpenLayers.Projection("EPSG:900913"), new OpenLayers.Projection("EPSG:4326"));
		input_lng_lat(c.x,c.y, mappa);
		revgeocod(c.x, c.y, mappa);
	});
  
});

function modcoo(lng, lat, mappa) {
    mappa.setCenter(new OpenLayers.LonLat(lng,lat).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913")), 13);
	var c = new OpenLayers.Geometry.Point(lng,lat).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913"));
	{{ module }}.layers.vector.addFeatures([new OpenLayers.Feature.Vector(c)]);
}

function input_lng_lat(lng, lat, mappa) {
	django.jQuery("#id_longitude").val(lng.toFixed(6));
	django.jQuery("#id_latitude").val(lat.toFixed(6));
}

function geocod(ind, mappa) {
	var geocoder = new google.maps.Geocoder();
	geocoder.geocode({'address': ind} ,
        function(results,status) { 
			if (status == google.maps.GeocoderStatus.OK) {
				if (status != google.maps.GeocoderStatus.ZERO_RESULTS) {
					lat = results[0].geometry.location.lat();  
					lng = results[0].geometry.location.lng(); 
					mappa.setCenter(new OpenLayers.LonLat(lng,lat).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913")), 13);
					var c = new OpenLayers.Geometry.Point(lng,lat).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913"));
					{{ module }}.layers.vector.addFeatures([new OpenLayers.Feature.Vector(c)]);
					input_lng_lat(lng, lat, mappa);
				}	
			}
			else {
				alert("Address not found!");
			}
        }
	)  
};

function revgeocod(lng, lat, mappa) {
	var geocoder = new google.maps.Geocoder();
	var infowindow = new google.maps.InfoWindow();
	var latlng = new google.maps.LatLng(lat,lng);
    geocoder.geocode({'latLng': latlng}, function(results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			django.jQuery("#id_address").val(results[0].formatted_address);
		} else {
			alert("Geocoder failed due to: " + status);
		}
	});
};	
	
{% endblock %}