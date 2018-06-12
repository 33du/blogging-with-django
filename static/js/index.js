$(document).ready(function() {
  $(window).on('scroll', loadOnScroll);

  var tag = "{{ tag_chosen }}";
  if (tag != null) {
    var tag_name = "{{ tag_chosen.name }}"
    $('.tag[id=' + tag_name + ']').addClass('active');
  }
});

function datetimeParse(datetime) {
  var date = datetime.split("T")[0];
  var time = datetime.split("T")[1];
  date = date.split("-");
  time = time.slice(0, -1);
  time = time.split(":");

  var month = parseInt(date[1]);
  month = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
  ][month];

  if (parseInt(time[0]) > 12) {
    var suffix = " p.m.";
    var hour = parseInt(time[0]) - 12;
  } else {
    var suffix = " a.m.";
    var hour = parseInt(time[0]);
  }

  if (date[2][0] == '0') {
    var day = date[2][1];
  } else {
    var day = date[2];
  }

  return month + " " + day + ", " + date[0] + ", " + hour + ":" + time[1] + suffix;
}

function strip(html)
{
   var tmp = document.createElement("DIV");
   tmp.innerHTML = html;
   return tmp.textContent || tmp.innerText || "";
}

// Scroll globals
var pageNum = 1; // The latest page loaded
var hasNextPage = true; // Indicates whether to expect another page after this one

// loadOnScroll handler
var loadOnScroll = function() {
   // If the current scroll position is past out cutoff point...
    if ($(window).scrollTop() > $(window).height() * 0.6) {
        // temporarily unhook the scroll event watcher so we don't call a bunch of times in a row
        $(window).off('scroll', loadOnScroll);
        // execute the load function below that will visit the JSON feed and stuff data into the HTML
        loadItems();
    }
};

var loadItems = function() {
    // If the next page doesn't exist, just quit now
    if (hasNextPage === false) {
        return false
    }
    // Update the page number
    pageNum = pageNum + 1;
    // Configure the url we're about to hit
    $.ajax({
        url: '',
        data: {page_number: pageNum},
        dataType: 'json',
        success: function(data) {
            // Update global next page variable
            hasNextPage = true;//.hasNext;
            // Loop through all items
            for (var i = 0; i < data.length; i++) {
              var post = data[i]

                $("#newItems").before(
                  '<div class="post">' +
                  '<h4>' + post['fields']['title'] + '</h4>' +
                  '<div class="post-time">' + datetimeParse(post['fields']['pub_time']) + '</div>' +
                  '<div class="post-text">' + strip(post['fields']['text']).substr(0, 200) + '</div>' +
                  '<a class="btn btn-outline-info btn-sm" href="' + post['pk'] + '/" role="button">Read more</a>' +
                  '</div>'

                );
            }
        },
        error: function(data) {
            // When I get a 400 back, fail safely
            hasNextPage = false
        },
        complete: function(data, textStatus){
            // Turn the scroll monitor back on
            $(window).on('scroll', loadOnScroll);
        }
    });
};
