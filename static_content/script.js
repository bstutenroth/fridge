function log(){
  alert("New food added!")
}

function button(){
  $('#submitbutton').on('click',log);
}

$(document).ready(button);
