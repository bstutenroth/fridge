function log(){
  alert("you did it!")
}

function button(){
  $('#submitbutton').on('click',log);
}

$(document).ready(button);
