$(function() {
	// Navbar toggle button
	$(".navbar-toggle-button").click("on", function(){
		slideout.toggle();
	});

	// Slideout menu
	var slideout = new Slideout({
		'panel': document.getElementById('main'),
		'menu': document.getElementById('menu'),
		'padding': 256,
		'tolerance': 70
	});
});

function rsvpAll() {
	$('#rsvpForm').append('<input type="hidden" name="rsvp_type" value="rsvp_all" />');
}