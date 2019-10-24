var buzzword_display = document.getElementById("buzzword_holder"); // html element containing
window.onload = function() {
	$("#buzzword_holder").css("opacity", 0.0);
	buzzword_display.innerHTML = buzzwords[0];
	function textSequence(i) {
		if (buzzwords.length > i) {
			setTimeout(function() {
				buzzword_display.innerHTML = buzzwords[i];
				$("#buzzword_holder").fadeTo(2000, 1, function() {
					$("#buzzword_holder").fadeTo(2000, 0);
				});
			textSequence(++i);
			}, 4000);
		} else if (buzzwords.length == i) {
			textSequence(0);	
		}
	}
	textSequence(1);
}
/* I opted to use the opacity  and fadeto rather than fadein/fadeout
because it resulted in better performance and ironed out some timing
related issues.
*/