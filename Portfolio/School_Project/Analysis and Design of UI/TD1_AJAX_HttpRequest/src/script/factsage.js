/*
 * Appel AJAX
 */
function loadDoc(idDoc) {
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = function () {
    /* 
     * readState = 4: requette terminer, larequest reponse est prette
     * status = 200: les status est ok
     */ 
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("page").innerHTML = this.responseText;
    }
  };
  xmlhttp.open("GET", idDoc, true);
  xmlhttp.send();
}

/*
 * Fonction permettant de "toggle" entre visible et invisible pour un menu "dropdown"
 */
function dropDownToggle(elementId) {
  document.getElementById(elementId).classList.toggle("show");
}

/*
 * Fonction qui permet de fermet le menu vertical si on click a lexterieur du menu
 */
window.onclick = function (event) {
  // si la zone negale pas celle du menu
  if (!event.target.matches('.container_menuIcon')) {

    var dropdowns = document.getElementsByClassName("container_verticalbar");
    var i;
    //Parcours la longeur de l'element "container_verticalbar" et fait en sorte qu'il soit tousse invisible en inversent la methode "dropDownToggle"
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}