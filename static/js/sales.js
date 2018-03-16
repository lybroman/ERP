$(document).ready(function(){
	
	$(".download-post").on("click", function(evt){
	var target = $(this).attr('data-src')
	alert(target)
	$.ajax({
			   type: "POST",
			   url: "/ERP/sales_form/",
			   contentType:"application/json",
			   data: JSON.stringify({"operation":"download",
									 "target": target}),
			   dataType:"json",
			   //async: false,
			   success: function(data){
				$(".overview-wrapper").hide()
				alert(JSON.stringify(data))
			   },
			   error: function(msg){
				   alert('Error:' + msg.responseText)
			   }
		});
	
	})
})
