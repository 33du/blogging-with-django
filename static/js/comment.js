$(document).ready(function() {
  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
  });

  $(".comment-btn").click(function(){
      $("#comment-modal").modal();

      if ($(this).is(".reply-btn")) {
        var parent_id = $(this).parent().attr('id');
        $("#id_parent_id").val(parent_id);
      }

  });

  $('.child-reply-btn').click(function(){
    $(this).parent().parent().parent().prev().find(".reply-btn").click();
  });

  $(".hide-btn").click(function(){
      $(this).parent().next().toggle();
      if ($(this).html() == 'show comments') {
        var scroll = $(window).scrollTop();
        $(this).html('&rarr;');
        $(this).parent().css({"text-decoration": "none", "padding-left": "0"})
        $(window).scrollTop(scroll);
        return false;
      } else {
        var scroll = $(window).scrollTop();
        $(this).html('show comments');
        $(this).parent().css({"text-decoration": "underline", "padding-left": "1rem"});
        $(window).scrollTop(scroll);
        return false;
      }
  });

  $(".delete-btn").click(function(){
    var result = confirm("Are you sure?");
    if (result) {
      $.ajax({
          type: 'POST',
          url: '/posts/comment/delete/',
          data: { 'comment_id': $(this).parent().attr('id') },
          success: function (response) {
            if (response.has_error) {
              alert("You cannot delete that!");
            } else {
              var scroll = $(window).scrollTop();
              location.reload();
              $(window).scrollTop(scroll);
              return false;
            }
          }
      });
    }
  });

  $("#comment-form").submit(function(e) {
    var form = $('#comment-form');
    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        success: function (response) {
          if (response.has_error) {
            $("#error-msg").html("<span class='badge badge-pill badge-danger'>!</span> "+ response.error_msg);
          } else {
            $("#comment-modal").modal('toggle');
            var scroll = $(window).scrollTop();
            location.reload();
            $(window).scrollTop(scroll);
            return false;
          }
        }
    });
    return false;
  });

});
