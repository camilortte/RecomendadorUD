   


    var bestPictures = new Bloodhound({
      datumTokenizer: function (d) {
                return Bloodhound.tokenizers.whitespace(d.value);
            },
      queryTokenizer: Bloodhound.tokenizers.whitespace,
      prefetch: '/buscar_json',
      remote:   {
            url: '/buscar_json',
            filter: function (data) {
                query=$("#id_qs").val();  
                return data.results
            },
            ajax: {
                type: 'GET',
                data: {
                    q: function(){
                        return $('#id_qs').val();
                    }
                },

            },
            replace: function(url, query) {
                return url + "#" + query; // used to prevent the data from being cached. New requests aren't made without this (cache: false setting in ajax settings doesn't work)
            }
        }
    });
     
    bestPictures.initialize();

    ;(function (_) {
        'use strict';

        _.compile = function (templ) {
            var compiled = this.template(templ);
            compiled.render = function (ctx) {
                return this(ctx);
            }
            return compiled;
        }
    })(window._);

    $('#remote .typeahead').typeahead(null, {
      name: 'best-pictures',
      displayKey: 'nombre',
      templates: {
        suggestion:  _.compile([
          '<p class="repo-language"  style="color:black;"><strong  style="color:black;"> <a  style="color:black;" href="/establecimientos/<%=id%>"><%=nombre%></a></strong></p>'       
        ].join(''))
      },
      source: bestPictures.ttAdapter()
    });


    $("#notificaciones").popover({
  'title' : "<p style='color:black;'>Notificaciones</p>", 
  'html' : true,
  'placement' : 'bottom',
  'content':$('.alert_list').html(),
  'placement': 'bottom',
  'animation': 'true',
  'container': '.navbar-nav'

});

if ($('#notification_content').html()){
      $('.top-left').notify({
        message: { html:  $('#notification_content').html()},
        fadeOut: { enabled: true, delay: 5000 }
      }).show(); // for the ones that aren't closable and don't fade out there is a .hide() function.
    }

$('#enviar_form').click(function(){
  $('#search_form').submit()
})

$("#id_qs").keypress(function(event) {
    if (event.which == 13) {
        event.preventDefault();
        $('#search_form').submit()
    }
});