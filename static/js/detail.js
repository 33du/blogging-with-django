$(document).ready(function() {
  $(".carousel-indicators > li:first").addClass("active");
  $(".carousel-item:first").addClass("active");

  var badges = ["badge-success",
                "badge-info",
                "badge-warning",
                "badge-danger",
                "badge-secondary",
                "badge-primary"
                ];

  for (var i = 0; i < $(".info-container span").length; i++) {
    var badge = badges[i % badges.length];
    $('.badge[id=' + i + ']').addClass(badge);
  }

});
