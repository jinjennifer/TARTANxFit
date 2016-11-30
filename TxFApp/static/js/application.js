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

$(function() {
	$( ".datepicker" ).datepicker();
});


// PushCrew notification
// (function(p,u,s,h){
//     p._pcq=p._pcq||[];
//     p._pcq.push(['_currentTime',Date.now()]);
//     s=u.createElement('script');
//     s.type='text/javascript';
//     s.async=true;
//     s.src='https://cdn.pushcrew.com/js/244437e6d1b60985b3819946fa71d802.js';
//     h=u.getElementsByTagName('script')[0];
//     h.parentNode.insertBefore(s,h);
// })(window,document);