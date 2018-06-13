$(document).ready(function() {
  $(".loginlink").click(function(){
      $("#loginmodal").modal();
  });

  $(".registerlink").click(function(){
      $("#registermodal").modal();
  });

  $("#loginForm").submit(function(e) {
    var form = $('#loginForm')
    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        success: function (response) {
          if (response.has_error) {
            $("#errorMsg").html("<span class='badge badge-pill badge-danger'>!</span> "+ response.error_msg);
          } else {
            $("#loginmodal").modal('toggle');
            location.reload();
          }
        }
    });
    return false;
  });

  $("#registerForm").submit(function(e) {
    var form = $('#registerForm')
    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        success: function (response) {
          if (response.has_error) {
            $("#errorMsg2").html("<span class='badge badge-pill badge-danger'>!</span> "+ response.error_msg);
          } else {
            $("#registermodal .modal-body").html("<p class='success'>Registration successful!<br><button type='button' class='btn btn-default my-btn' data-dismiss='modal'>Close</button></p>");
          }
        }
    });
    return false;
  });

  var pathname = window.location.pathname;
	$('.nav-link[href="'+pathname+'"]').parent().addClass('active');
});
