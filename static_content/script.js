//listners
function associate_events(){
  $("#submitbutton").click(button);
}

$(document).ready(associate_events);

//when clicking submit button, check
function button(){
  window.alert("New food recorded!");
}

function make_bigger(){
  console.log('make_bigger')
  $(this).css({'padding' : '3%'});
  // $(this > '.hidedate').show();

}
function back_to_origional(){
  console.log("back_to_origional");
    $(this).css({'padding' : '1%'});
    // $(this > '.hidedate').hide();

}
function hide_date(){
  console.log("hide_date")
  $(this).find(".hidedate").hide();
}
function show_date(){
  console.log("show_date")
$(this).find(".hidedate").show();
}

$(document).ready(setup1);

function setup1(){
  $('.foodCat').hover(make_bigger, back_to_origional);
  if (top.location.pathname === '/myfridge'){
    $('.hidedate').hide();
  }
  $('.foodCat').hover(show_date, hide_date);
  // $('.hidedate').hover(make_bigger, back_to_origional);
}
