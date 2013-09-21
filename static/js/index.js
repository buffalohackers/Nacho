$(document).ready(function(){

    $( "ul.droptrue" ).sortable({
      connectWith: "ul"
    });
 
    $( "#active-speakers, #available-speakers" ).disableSelection();
});