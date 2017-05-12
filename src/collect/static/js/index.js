let words = [];

setInterval(() => {
  if (words.length === 0) {
    return;
  }
  post('/words', {words});
}, 1000);

monitor('#editarea', word => words.push(word));
