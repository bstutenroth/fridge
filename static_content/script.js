//listners
function associate_events(){
  $("#submitbutton").click(button);
}

$(document).ready(associate_events);

//when clicking submit button, check
function button(){
  window.alert("New food recorded!");
}
