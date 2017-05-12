$(document).ready(() => {
  $('.char').each((i, el) => {
    let elt = $(el);
    let char = String.fromCharCode(elt.data('keycode'));
    elt.html(char);
  });
});
