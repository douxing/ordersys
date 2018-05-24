function open_image_chooser(e) {
  var event = e ? e : window.event;
  event.stopPropagation();
  event.preventDefault();

  document.querySelector("#overlay").style.display = 'block';

  $.ajax({
    url: '/menuicons',
    type: 'GET',
    success: function(data, textStatus, jqXHR) {
      var grid = $("#image-grid");
      grid.empty();

      data.forEach(function(name) {
        var path = "/static/menuicons/" + name;

        var img = $('<img src="' + path + '"' + ' />');

        img.click(function () {
          $("#icon_hashname").attr('value', name);
          $("#preview_icon").attr('src', path);
        });

        grid.append(img);
      });
    },
    error: function(jqXHR, textStatus, errorThrown) {
      alert('请重试!');
    },
  });
}

function close_image_chooser(e) {
  var event = e ? e : window.event;
  event.stopPropagation();
  event.preventDefault();

  document.querySelector("#overlay").style.display = 'none';
}

function choose_image(e) {
  var event = e ? e : window.event;
  event.stopPropagation();
  event.preventDefault();

  document.querySelector("#image_url").value="hello";
  document.querySelector("#overlay").style.display = 'none';
}
