/************************************************************************************/
/* Title : script.js																*/
/* Author : Jean-Simon Marrocco														*/
/* Date : 2017																		*/
/* Description:																		*/
/*				- Help generate DOM for certain part								*/
/*				- Enable a smooth scrolling when the navbar buttons are press		*/
/*				- Update text font-size when the window is resize					*/
/************************************************************************************/
$(document).ready(function () {

	resizeTitle();
	smoothScrolling();
	generateEquipe();

});

//generate the HTML for the team cards 
function generateEquipe(){
	
	//Teammate Information
	var data = '{"equipe":[' +
		'{"title":"Président", "name":"William Savard", "mail":"william.savard@polymtl.ca", "avatar":"president.jpg"},' +
		'{"title":"Vice-présidente à la conception", "name":"Jasmine Saint-Vincent", "mail":"jasmine.saint-vincent@polymtl.ca", "avatar":"vp_conception_1.jpg"},'+
		'{"title":"Vice-présidente à la conception", "name":"Katerie Coudé", "mail":"katerie.coude@polymtl.ca", "avatar":"vp_conception_2.jpg"},'+
		'{"title":"Vice-présidente à la rédaction de l’EDP", "name":"Anamaria Serbescu", "mail":"anamaria.serbescu@polymtl.ca", "avatar":"vp_redaction.jpg"},'+
		'{"title":"Vice-présidente à la logistique", "name":"Stéphanie Vigeant", "mail":"stephanie.vigeant@polymtl.ca", "avatar":"vp_logistique.jpg"},'+
		'{"title":"Trésorier", "name":"Romulo Henriquez", "mail":"romulo-rafael.henriquez-torres@polymtl.ca", "avatar":"basicAvatar.jpg"},'+
		'{"title":"Secrétaire", "name":"Brian Rutherford", "mail":"brian.rutherford@polymtl.ca", "avatar":"secretaire.jpg"}]}';
	teamInfo = JSON.parse(data);
	
	var team = document.getElementById("NotreEquipe");
	var row = documment = document.createElement("div");
	row.className="row";
	
	team.appendChild(row);
	
	nbrTeammate = teamInfo.equipe.length;
	
	//For every teammate generate the DOM of the card
	for(var i = 0; i < nbrTeammate; i++){
		
		//step 1: create the different elements
		var col = documment = document.createElement("div");
		col.className="col-sm-4 card-col"; 	
		
		var teammate = teamInfo.equipe[i];
		
		var card = document.createElement("div");
		card.className="card";
		
		
		var avatar = document.createElement("img");
		avatar.className = "card-img-top";
		avatar.src = "./src/img/avatar/" + teammate.avatar;
		
		var cardBody = document.createElement("div");
		cardBody.className = "card-body";
		
		var Name= document.createElement("h4");
		Name.className = "card-title";
		Name.innerHTML = teammate.name;
		
		var title = document.createElement("p");
		title.className = "card-text";
		title.innerHTML = teammate.title;
		
		var mail = document.createElement("p");
		mail.className = "card-text";
		mail.innerHTML = teammate.mail;
		
		
		//step 2: line up the DOM
		row.appendChild(col);
		col.appendChild(card);
		card.appendChild(avatar);
		card.appendChild(cardBody);
		cardBody.appendChild(Name);
		cardBody.appendChild(title);
		cardBody.appendChild(mail);
		
	}

}

//For a smooth Scrolling when a navbar button is use
function smoothScrolling(){
		// Add smooth scrolling to all links in navbar + footer link
	$(".navbar a, footer a[href='#myPage']").on('click', function(event) {

	// Make sure this.hash has a value before overriding default behavior
	if (this.hash !== "") {

	// Prevent default anchor click behavior
	event.preventDefault();

	// Store hash
	var hash = this.hash;

	// Using jQuery's animate() method to add smooth page scroll
	// The optional number (900) specifies the number of milliseconds it takes to scroll to the specified area
	$('html, body').animate({
	  scrollTop: $(hash).offset().top
	}, 900, function(){

	  // Add hash (#) to URL when done scrolling (default click behavior)
	  window.location.hash = hash;
	  });
	} // End if 
	});
}

// This function resize the title (Chem-e-car) base 
// on the percentage of the window's width 
function resizeTitle(){
	//check if we are in a small screen first
	if ($( window ).width() <= 400){
		size = 20;
		$("#title").css({'font-size': size+'px'});
	} 
	else{	
		var resizePercentage = setResizePercentage();
		var size = $( window ).width()*resizePercentage;
		$("#title").css({'font-size': size+'px'});
	}
	
	//if the window is resize adjust the font-size 
	$(window).resize(function(){
		//find the right percentage to use
		resizePercentage = setResizePercentage();
		
		if ($( window ).width() >= 675){
			size = $( window ).width()*resizePercentage;
			$("#title").css({'font-size': size+'px'});
		}
		
	});
}

function setResizePercentage(){
	
	var percentage;
	
	if ($( window ).width() > 996){
			percentage = 0.035;
		}
		else if ($( window ).width() < 996 && $( window ).width() > 396){
			percentage = 0.03;
		}
		
		return percentage;
}