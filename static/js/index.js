$(document).ready(function(){

     var activeList = [];  
     var availableList = [];
     s = $("#owner").text().split(".");
     var owner = s[s.length-1];

    $('#available-speakers li').each(function(){
    	value = $(this).text();
    	availableList.push(value);
    });

    $('#active-speakers li').each(function(){
    	value = $(this).text();
    	activeList.push(value);
    });

    $( "#active-speakers, #available-speakers" ).sortable({
      connectWith: ".connected",
      stop: function(event, ui) {
      	original = $(event.target).attr("id");
    	name = event.toElement.innerHTML;
    	if (original == "available-speakers") {
    		postList(name, owner);
    	} else {
    		postList(name, -1);
    	}
      }
    }).disableSelection();
});

function postList(name, owner) {
 	$.ajax({
 		url: "https://localhost:1337/changeOwner",
 		async: false,
 		dataType: "application.json",
 		type: "POST",
 		data: {
 			"name": name,
 			"owner": owner 
 		}
 	}).done(function(data){
 		console.log(data);
 	});
 };