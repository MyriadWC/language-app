$(document).ready(function() {

   $("#pop").on("click", function() {
      $('#imagepreview').attr('src', $('#imageresource').attr('src')); // here asign the image to the modal when the user click the enlarge link
      $('#imagemodal').modal('show'); // imagemodal is the id attribute assigned to the bootstrap modal, then i use the show function
   });

   //Update likes when like button pressed
   $('.like-form').on('submit', function(event) {
     event.preventDefault();
     var form = $(this);
     var url = form.attr('action');
     var data = form.serialize();
     $.ajax({
       type: 'POST',
       url: url,
       data: data,
       success: function(response) {
         // Update the like count
         form.find('.like-count').text(response.total_likes);

         //Change button from outline to block
         form.find('button').toggleClass('btn-outline-dark btn-warning')
       }
     });
   });

 }); // End document ready