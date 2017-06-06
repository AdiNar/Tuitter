function onButton() {
    document.getElementById("btt").innerHTML = "TWIT";
    var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("twits").innerHTML =
      this.responseText;
    }
  };
  xhttp.open("GET", "/twits/twits_list", true);
  xhttp.send();
}

function submit_twit() {

}