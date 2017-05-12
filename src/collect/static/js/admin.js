function encode(word) {
  post('/encode', {word}).then(resp => $('#encoded').html(JSON.stringify(resp.encoded)));
}

monitor('#encode_input', encode);
