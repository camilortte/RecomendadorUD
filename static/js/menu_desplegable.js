
      var menuLeft = document.getElementById( 'cbp-spmenu-s1' ),
        showLeftPush = document.getElementById( 'showLeftPush' ),       
        body = document.body;
 
      
             
        showLeftPush.onclick = function() {            
            if ($('#icon_menu').is(":visible") ==true){
                $('#icon_menu').hide();
                $("#navbar_id").toggleClass('navbar-fixed-top navbar-static-top');
                $( 'body' ).css( "padding-top","0px" );
                console.log("No es visible");
                classie.toggle( this, 'active' );
                classie.toggle( body, 'cbp-spmenu-push-toright' );
                classie.toggle( menuLeft, 'cbp-spmenu-open' );    
            }
            
        };

        $( "#menu_boton" ).click(function() {
            $('#icon_menu').show();
            $("#navbar_id").toggleClass('navbar-static-top navbar-fixed-top');
            $( 'body' ).css( "padding-top","70px" );
            classie.toggle( this, 'active' );
            classie.toggle( body, 'cbp-spmenu-push-toright' );
            classie.toggle( menuLeft, 'cbp-spmenu-open' );
        });

        

