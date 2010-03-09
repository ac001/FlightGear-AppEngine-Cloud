/*$(document).ready(function(){
   $("#orderedlist").click(function(event){
     alert("Thanks for visiting!");
   });
 });
*/

function toggle_download(obj){
	var v = obj.value;

	if(v == 32){
		$('#down_32').slideDown('slow')
		$('#down_64').slideUp('slow')
	}else{
		$('#down_32').slideDown('slow')
		$('#down_64').slideDown('slow')
	}

}