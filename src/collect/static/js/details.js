$(document).ready(() => {
  $('.char').each((i, el) => {
    let elt = $(el);
    let char = String.fromCharCode(elt.data('keycode'));
    elt.html(char);
  });
});

function calc_mean_delays(word) {
  post(`/means/${window.id}`, {word}).then(resp => $('#means').html(JSON.stringify(resp.delays)));
}

monitor('#mean_input', calc_mean_delays);
