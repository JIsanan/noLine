$(window).scroll(function(){
	$('#site-landing-header').toggleClass('scrolled', $(this).scrollTop() > ($('#site-hero').height() - 96));
});

$("#next").click(function() {
	goToPage();
});

// hides the cards and pagination
function goToPage() {
	document.getElementsByClassName('feed-pagination')[0].style.display = "none";
	document.getElementsByClassName('feed-cards')[0].style.display = "none";
	document.getElementsByClassName('feed-card-loading')[0].style.display = "flex";
	$('html, body').animate({
    scrollTop: $("#site-feed").offset().top
  }, 500);
}
