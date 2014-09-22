function pops( message ){

	$('#response').prepend('<p>' + message + '</p>');
	$('#response').contents().fadeOut(1500);
	
};

function sendG(gcode, unit='mm', repeat=1){
  $.post("/g",
  {
    gcode:gcode,
    unit:unit,
    repeat:repeat
  },
  function(data,status){
	pops( data );
  });
};

function drawGcode(){
	

};

$('#convertButton').click(function(){
    var formData = new FormData($("form[name='convert']")[0]);
    $.ajax({
        url: '/convert',  //Server script to process data
        type: 'POST',
        // Form data
        data: formData,
        //Options to tell jQuery not to process data or worry about content-type.
        cache: false,
        contentType: false,
        processData: false
    })
     .success	(function( data ) {
      if(data.success[0] == true){
        console.log('conversion win')
				var code = [];
				for(i = 0; i < data.groups.length; i++){
					for(k = 0; k < data.groups[i].gcode.length; k++)
						code.push(data.groups[i].gcode[k]);
				}
				$("textarea[name='gcode']").val(code.join("\n"));
				pops(data.success[1]);
			} else {
			  console.log('conversion fail!');
			  pops( data.success[1] );
			};
		 });
});
