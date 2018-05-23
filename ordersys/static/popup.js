function open_image_chooser(e) {
  var event = e ? e : window.event;
  event.stopPropagation();
  event.preventDefault();

  document.querySelector("#overlay").style.display = 'block';
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
