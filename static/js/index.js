$(document).ready(function(){

	var activeList = [];  
	var availableList = [];
	s = $("#owner").text().split(".");
	var owner = s[s.length-1];
	var lastVolume = 50;

	setIds();

    $('#available-speakers li').each(function(){
    	value = $(this).text();
    	availableList.push(value);
    });

    $('#active-speakers li').each(function(){
    	value = $(this).text();
    	activeList.push(value);
    });

    $( ".volume-bar").slider({
      range: "min",
      value: lastVolume,
      min: 1,
      max: 100,
      stop: updateVolume
    });

    $( "#active-speakers, #available-speakers" ).sortable({
     	connectWith: ".connected",
      	stop: function(event, ui) {
      		current = $($(ui.item).context.parentNode).attr("id");
      		ipAddress = $(ui.item).attr("name");
      		id = $(ui.item).attr("id");
      		if (current == "available-speakers") {
      			if ($("#" + id + " div.volume-bar").length > 0) {
					$("#" + id + " .volume-bar").remove();
	    			$("#" + id + " .mute").remove();
	    			$("#" + id + " div").removeClass("pull-left");
	      			postList(ipAddress, -1);
	      		}
      		} else if (current == "active-speakers") {
      			if ($("#" + id + " > div.volume-bar").length <= 0) {
	      			$("#" + id + " > div.device-name").addClass("pull-left");
		    		$("#" + id).append("<div class='pull-right mute'>Mute</div><div class='volume-bar'></div>");
		    		$("#" + id + " > div.mute").bind("click", function(){
				    	if ($(this).hasClass("muted")) {
				    		$("#" + this.parentNode.id + " > div.volume-bar").slider( "value", lastVolume );		
				    		$("#" + this.parentNode.id + " > div.volume-bar").slider( "enable");		
				    		$(this).removeClass("muted");
				    		$(this).html("Mute");
				    		postVolume($(this.parentNode).attr("name"), lastVolume);
				    	} else {
							$(this).addClass("muted");
							$("#" + this.parentNode.id + " > div.volume-bar").slider( "value", 0 );		
							$("#" + this.parentNode.id + " > div.volume-bar").slider( "disable");		
							$(this).html("Muting");
				    		postVolume($(this.parentNode).attr("name"), 0);
				    	}
				    });
		    		$("#" + id + " > div.volume-bar").slider({
				      range: "min",
				      value: lastVolume,
				      min: 1,
				      max: 100,
				      stop: updateVolume
				    });
      				postList(ipAddress, owner)
	    		}
      		}
      	}
    }).disableSelection();

    $("div.mute").click(function(){
    	if ($(this).hasClass("muted")) {
    		$("#" + this.parentNode.id + " > div.volume-bar").slider( "value", lastVolume);		
    		$("#" + this.parentNode.id + " > div.volume-bar").slider( "enable");		
    		$(this).removeClass("muted");
    		$(this).html("Mute");
    		postVolume($(this.parentNode).attr("name"), lastVolume);
    	} else {
			$(this).addClass("muted");
			$(this).html("Muting");
			$("#" + this.parentNode.id + " > div.volume-bar").slider( "value", 0);		
			$("#" + this.parentNode.id + " > div.volume-bar").slider( "disable");		
    		postVolume($(this.parentNode).attr("name"), 0);
    	}
    });
});

function postList(name, owner) {
	console.log(name, owner);
 	$.post("http://localhost:1337/changeOwner",{"name": name,"owner": owner});
}

function updateVolume(event, ui) {
	name = $(ui.handle.parentNode.parentElement).attr("name");
    value = ui.value;
	postVolume(name, value);
}

function postVolume(name, value) {
	console.log(name, value);
	lastVolume = value;
	$.post("http://localhost:1337/updateVolume", {"name": name, "volume": lastVolume});
}

function setIds(){
	$("#available-speakers li").each(function(){
		reformatId(this);
	});
	$("#active-speakers li").each(function(){
		reformatId(this);
	});
}

function reformatId(that){
	if ($(that).context.childElementCount > 0) {
		ip = $(that).attr("id");
		id = ip.replace(/\./g, "-");
		$(that).attr("id", id);
		$(that).attr("name", ip);
	}
}
