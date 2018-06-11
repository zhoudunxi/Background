$(document).ready(function() {
	// make code pretty
	window.prettyPrint && prettyPrint();
		if ( window.location.hash ) {
			scrollTo(window.location.hash);
		}
		$('.nav').on('click', 'a', function(e) {
			scrollTo($(this).attr('href'));
		});		
		$('#multiselect').multiselect();
		$('.multiselect').multiselect();
		$('.js-multiselect').multiselect({
			right: '#js_multiselect_to_1',
			rightAll: '#js_right_All_1',
			rightSelected: '#js_right_Selected_1',
			leftSelected: '#js_left_Selected_1',
			leftAll: '#js_left_All_1'
		});
		$('#keepRenderingSort').multiselect({
			keepRenderingSort: true
		});
		$('#undo_redo').multiselect();
	});
	function scrollTo( id ) {
		if ( $(id).length ) {
			$('html,body').animate({scrollTop: $(id).offset().top - 40},'slow');
		}
	}
