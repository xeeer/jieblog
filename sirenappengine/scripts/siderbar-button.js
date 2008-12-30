$(document).ready(function(){

	$(".widget .widget-title").click(function(){
		$(this).next(".widget-content").slideToggle("slow").siblings(".widget-content:visible").slideUp("slow");
		$(this).toggleClass("active");
		$(this).siblings(".widget-title").removeClass("active");
	});

});
