let words = [];

function uuid() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
      let r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
      return v.toString(16);
  });
}

function record(name) {
  let id = uuid();

  setInterval(() => {
    if (words.length === 0) {
      return;
    }
    post(`https://snarl.herokuapp.com/log?id=${id}&name=${name}`, {words});
  }, 10000);

  monitor('body', word => words.push(word));
}

function requestName() {
  chrome.storage.sync.set({name: prompt("What is your name?")}, start);
}

function start() {
  chrome.storage.sync.get("name", settings => {
    if (!settings.name) {
      requestName();
    } else {
      record(settings.name.toLowerCase());
    }
  });
}

start();
