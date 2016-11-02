$(function() {
	// Navbar toggle button
	$(".navbar-toggle-button").click("on", function(){
		slideout.toggle();
	});

	// Slideout menu
	var slideout = new Slideout({
		'panel': document.getElementById('panel'),
		'menu': document.getElementById('menu'),
		'padding': 256,
		'tolerance': 70
	});
});