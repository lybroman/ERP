$(document).ready(function(){
	$(".download-post").on("click", function(){
		var target = $(this).attr('data-src')
		var uuid  = $('#uuid').val()
		var post_data = {"operation":"download",
									 "target": target,
									 "uuid" : uuid}
		post_data_content = 'operation=' + JSON.stringify(post_data)
		//alert(post_data_content)
		$.download('/ERP/sales_statistics_form/', post_data_content, 'post' )
	});
	
	$("#unit").change(function(evt){
			var re = /^[0-9]+.?[0-9]*$/;
			if (!re.test($("#unit").val()) || !re.test($("#amount").val()))
			{
				$("#total").val(-1)
			}
			else
			{
				$("#total").val(parseFloat($("#unit").val()) * parseFloat($("#amount").val()))
			}
			
		})
		
		$("#amount").change(function(evt){
			var re = /^[0-9]+.?[0-9]*$/;
			if (!re.test($("#unit").val()) || !re.test($("#amount").val()))
			{
				$("#total").val(-1)
			}
			else
			{
				$("#total").val(parseFloat($("#unit").val()) * parseFloat($("#amount").val()))
			}
			
		})
		
	$("#currency_rate").change(function(evt){
			var re = /^[0-9]+.?[0-9]*$/;
			if (!re.test($("#currency_rate").val()))
			{
				alert("Invalid currency rate!")
				$("#currency_rate").val(1.0)
			}
			
		})

});

jQuery.download = function(url, data, method){
    if( url && data ){ 
        data = typeof data == 'string' ? data : jQuery.param(data);
        var inputs = '';
        jQuery.each(data.split('&'), function(){ 
            var pair = this.split('=');
            inputs+="<input type='hidden' name='"+ pair[0] +"' value='" + pair[1] +"' />"
			//alert(inputs)
        });
        jQuery('<form action="'+ url +'" method="'+ (method||'post') +'">'+inputs+'</form>')
        .appendTo('body').submit().remove();
    };
};