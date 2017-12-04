$(document).ready(function () {
    $('#tags').val(""); // efface contenue de la bar de recherche

    /*
     * Reload la page web lorsque le button Acceuil est appuyee
     */
    $('#Acceuil').click(function() {
        location.reload();
    });

    /*
     * Tabs toggle animatio
     * Rend le contenue visible;
     */
    $(".nav-link.active").css("color", "white");
    $(".nav-link.active").css("background-color", "#01DF3A");
    $(".section").click(function () {
        $(".section").css("background-color", "rgba(0, 0, 0, 0)");
        $(".section").css("color", "#289eca");
        $(this).css("color", "white");
        $(this).css("background-color", "#01DF3A");
        // $(this).tab('show');
    });


    /*
     * get json file content
     */
    var stations = new Array();
    var stationsVelosName = new Array();
    var tableauStations = new Array();

    $.getJSON("http://secure.bixi.com/data/stations.json", function (result) {
        $.each(result.stations, function (index, element) {
            stations[index] = element
            stations[index].b = changeBooleanToTextValue(stations[index].b);
            stations[index].su = changeBooleanToTextValue(stations[index].su);
            stations[index].m = changeBooleanToTextValue(stations[index].m);
            stationsVelosName[index] = stations[index].s   
            
            tableauStations[index] = new Array(stations[index].id, stations[index].s, stations[index].ba, stations[index].da, stations[index].b, stations[index].su); 

        }); 
        $('#tableauStation').DataTable( {
        data: tableauStations,
        columns: [
            { title: "ID" },
            { title: "Nom Station" },
            { title: "Vélos disponibles" },
            { title: "Bornes disponibles" },
            { title: "État bloquée" },
            { title: "État suspendue" }
        ]
    } );
    });

    $("#tags").autocomplete({
        source: stationsVelosName
    });


    $('#ui-id-1').click(function () {
        generateStationInfo(stations);
    });
    //check event si button enter est up
    $("#tags").on('keyup', function (e) {
        if (e.keyCode == 13) {
            generateStationInfo(stations);
        }
    });
    
    /*
     *Methode pour generer l'information sur la station choisi
     */
    function generateStationInfo(stations) {
      $("#ui-id-1").css("display", "none");

      //Animation pour centrer l'information
      $( "#tags" ).animate({
          margin: '20px 0px 0px 15%'  
      }, 1000 );
        
      $(".stationInfo").css("display", "block");
      
      //afficher linformation
      var selectStationName = $('#tags').val();
      var station = stations[stationsVelosName.indexOf(selectStationName)];
      
      $('#stationName').text(selectStationName);
      $('#idStation > p').text(station.id);  
      $('#bloquee > p').text(station.b);
      $('#suspendue > p').text(station.su);
      $('#hs > p').text(station.m);
      $('#velosDispo > p').text(station.ba);
      $('#bornesDispo > p').text(station.da);
      $('#velosIndispo > p').text(station.bx);
      $('#bornesIndispo > p').text(station.dx);
      
      $('#velosDispo > p').css("background-color",getColorFromValue(station.ba));     
      $('#bornesDispo > p').css("background-color",getColorFromValue(station.da));    
      $('#bloquee > p').css("background-color",getColorFromValue(station.b));    
      $('#suspendue > p').css("background-color",getColorFromValue(station.su));
      $('#hs > p').css("background-color",getColorFromValue(station.m));
          
        /*
         * Generate m google map
         */
        var latLng = new google.maps.LatLng({
            lat: stations[stationsVelosName.indexOf(selectStationName)].la,
            lng: stations[stationsVelosName.indexOf(selectStationName)].lo
        });
        var map = new google.maps.Map(document.getElementById('map'), {
            center: latLng,
            zoom: 11
        });
        marker = new google.maps.Marker({
            position: latLng,
            map: map
        });
    }
    
    function getColorFromValue(value){
      if(value == '0' || value == 'oui'){
          return 'red';
        }else{
          return '#01DF3A';
      }
    }
    
    function changeBooleanToTextValue(state){
      if(state == true){
            return 'oui';
        }else{
            return 'non';
        }
    }
});