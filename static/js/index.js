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
      	name = event.toElement.id;
    	if (original == "available-speakers") {
    		postList(name, owner);
    	} else {
    		console.log(owner);
    		postList(name, -1);
    	}
      }
    }).disableSelection();

    $( ".volume-bar").slider({
      range: "min",
      value: 50,
      min: 1,
      max: 100,
      stop: function(event, ui) {
      	name = ui.handle.parentNode.parentElement.id;
        value = ui.value;
        updateVolume(name, value);
      }
    });

    $(".mute").click(function(){
    	if ($(this).hasClass("muted")) {
    		console.log($("#" + this.parentNode.id + " .volume-bar"));
    		$("#" + this.parentNode.id + " .volume-bar").slider( "value", 50 );		
    		updateVolume(this.parentNode.id, 50);
    	} else {
			$(this).addClass("muted");
			$("#" + this.parentNode.id + " .volume-bar").slider( "value", 0 );		
    		updateVolume(this.parentNode.id, 0);
    	}
    });
});

function postList(name, owner) {
	console.log(name, owner);
 	$.post("http://localhost:1337/changeOwner",{"name": name,"owner": owner});
}

function updateVolume(name, volume) {
	console.log(name, volume);
	$.post("http://localhost:1337/updateVolume", {"name": name, "volume": volume});
}