function evaluate(password) {
  let username = $('#username').val();
  post('/evaluate', {username, password}).then(resp =>
    $('#response').html(`[${resp.likelihood}] ${resp.success ? 'Success!' : 'Failed :('}`)
  );
}

monitor('#password', evaluate);
