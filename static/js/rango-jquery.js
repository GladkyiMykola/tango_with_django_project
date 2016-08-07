$(document).ready( function() {

   $("#about-btn").addClass('btn btn-primary').click( function(event) {
        alert("You clicked the button using JQuery!");
    });

    $("p").hover( function() {
            $(this).css('color', 'red');
    },
    function() {
            $(this).css('color', 'blue');
    });


});
