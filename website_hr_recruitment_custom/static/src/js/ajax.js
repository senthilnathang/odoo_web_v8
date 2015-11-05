$(document).ready(function(){
	$("#bt").on('click', function(e){
		mobile()
	});
	
	//$("#frm1").submit(validatefrm);
	
}); 
function showbtn()
{

document.getElementById("year").style.display = "block";
document.getElementById("month").style.display = "block";

}

function hidebtn()
{

document.getElementById("year").style.display = "none";
document.getElementById("month").style.display = "none";

}
function mobile()
{
	alert("Hiiiiii");
	var mb=document.frm1.mobile.value;
	if(isNaN(mb))
    {
        alert ("please enter the only number");
	
        $("#mobile").focus();
        return false;
    }
}
