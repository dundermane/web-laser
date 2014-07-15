$("#down").click(function(){
  $.post("/g",
  {
    gcode:"G91\nG0X0Y-0.5\nG90",
    unit:"in",
    repeat:"1"
  },
  function(data,status){
	$('#response').prepend('<p>' + data + '</p>');
	$('#response').contents().fadeOut(1500);
  });
});

$("#up").click(function(){
  $.post("/g",
  {
    gcode:"G91\nG0X0Y0.5\nG90",
    unit:"in",
    repeat:"1"
  },
  function(data,status){
	$('#response').prepend('<p>' + data + '</p>');
	$('#response').contents().fadeOut(1500);
  });
});

$("#right").click(function(){
  $.post("/g",
  {
    gcode:"G91\nG0X0.5Y0\nG90",
    unit:"in",
    repeat:"1"
  },
  function(data,status){
	$('#response').prepend('<p>' + data + '</p>');
	$('#response').contents().fadeOut(1500);
  });
});

$("#left").click(function(){
  $.post("/g",
  {
    gcode:"G91\nG0X-0.5Y0\nG90",
    unit:"in",
    repeat:"1"
  },
  function(data,status){
	$('#response').prepend('<p>' + data + '</p>');
	$('#response').contents().fadeOut(1500);
  });
});

$("#stop").click(function(){
  $.post("/g",
  {
    gcode:"M5",
    unit:"in",
    repeat:"1"
  },
  function(data,status){
	$('#response').prepend('<p>' + data + '</p>');
	$('#response').contents().fadeOut(1500);
  });
});


$("#on").click(function(){
  $.post("/g",
  {
    gcode:"M3",
    unit:"in",
    repeat:"1"
  },
  function(data,status){
	$('#response').prepend('<p>' + data + '</p>');
	$('#response').contents().fadeOut(1500);
  });
});

$("#gsend").click(function(){
  $.post("/g",
  {
    gcode: $('textarea[name=gcode]').val(),
    unit: $('input[name=unit]:radio:checked').val(),
    repeat: $('input[name=repeat]').val()
  },
  function(data,status){
	$('#response').prepend('<p>' + data + '</p>');
	$('#response').contents().fadeOut(1500);
  });
});
