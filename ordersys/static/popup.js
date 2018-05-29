function open_image_chooser(e) {
  var event = e ? e : window.event;
  event.stopPropagation();
  event.preventDefault();

  document.querySelector("#overlay").style.display = 'block';

  $.ajax({
    url: '/course/menuicons',
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

function dec_qty(e, id) {
  var event = e ? e : window.event;
  event.stopPropagation();
  event.preventDefault();

  var elem = $("#qty_" + id);

  var num = Number.parseInt(elem.attr('value'));
  if (Number.isNaN(num)) {
    elem.attr('value', "0");
  } else {
    num = Math.max(0, num - 1);

    elem.attr('value', "" + num);
  }
}

function inc_qty(e, id) {
  var event = e ? e : window.event;
  event.stopPropagation();
  event.preventDefault();

  var elem = $("#qty_" + id);

  var num = Number.parseInt(elem.attr('value'));
  if (Number.isNaN(num)) {
    elem.value = "0";
  } else {
    num = Math.min(1000000000, num + 1);

    elem.attr('value', "" + num);
  }
}
