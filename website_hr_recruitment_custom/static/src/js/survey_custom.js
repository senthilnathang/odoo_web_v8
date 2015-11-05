/* My code
var news = $('.news')
current = 0;
prev = 1;
news.hide();


$('#btexam').click(function() {
    $('#btnext').show();
    $('#btexam').hide();
    $('#btnext').click(function() {
    Rotator();});
});



function Rotator() {
    if ((news.length-1) !== current){
        $(news[current]).show();
        if (prev !== 0){
            $(news[prev]).hide();
        }else{
            $(news[0]).hide();
        }
        $(news[current]).queue(function() {
            current = current < news.length - 1 ? current + 1 : 0;
            prev = current < news.length + 1 ? current - 1 : 0; 
            //Rotator();
            //$(this).dequeue();
        });
    }else{
        $('#btnext').hide();
        $('.finish').show();
 }
}
*/



 var news = $('.news')
current = 0;
prev = 1;
news.hide();



    $('#btexam').click(function() {
	
    Rotator();
	$('#btnext').show();
	$('#btexam').hide();
	 $('#btnext').click(function() {
	$('.tim').timer('reset');
	
    Rotator(true);
	//document.getElementsByClassName("row js_radio")[0].disabled = true;
	//document.getElementsByClassName("row js_radio").readOnly=true;
		});
	});


$('.finish').click(function() {
    news.hide();
    
    $('.shiw').show();
});


function Rotator(bDisabled) {
	//$('.tim').timer('reset');
	//document.getElementsByClassName("row js_radio").readOnly=true;
	var selects = document.getElementsByTagName("div");
    $(":radio").attr('disabled',false);
	//console.log("selects....===",selects);
    if ((news.length-1) !== current){
        $(news[current]).show();
	
       
        $('.tim').timer({
          duration: '60s',
          callback: function() {
	  
	  alert('Time up!');
	  $('.tim').timer('pause');
	  //$('.news').hide();
	  //$('.news').disabled = bDisabled;
	  //$('.news').disabled = true;
	  //$('.news').readOnly = true;
	  //document.forms[0].elements[6].readOnly = true;
	  //document.forms[0].elements[6].disabled = bDisabled;
	  $(":radio").attr('disabled','disabled');
			 
	  console.log("pahonchyu disable ni niche...!!!!");
	  
	  		},
	 });
	//document.getElementsByClassName("js_radio").disabled = true;
	//$(".news").attr("readonly", "1");
       
        if (prev !== 0){
            $(news[prev]).hide();
        }else{
            $(news[0]).hide();
        }
        $(news[current]).queue(function() {
            current = current < news.length - 1 ? current + 1 : 0;
            prev = current < news.length + 1 ? current - 1 : 0; 
            //Rotator();
            //$(this).dequeue();
		/*$(tim[current]).queue(function() {
            current = current < tim.length - 1 ? current + 1 : 0;
            prev = current < tim.length + 1 ? current - 1 : 0; 
            
        			}); */
        });
	/*$(tim[current]).queue(function() {
            current = current < tim.length - 1 ? current + 1 : 0;
            prev = current < tim.length + 1 ? current - 1 : 0; 
            
        });*/
    }else{
        $('#btnext').hide();
	$('.tim').hide();
        $('.finish').show();
 }
$('.finish').click(function() {
    $('.finish').hide();});
}


