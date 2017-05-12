const SPACEBAR = 32;

class Character {
  constructor(keyCode) {
    this.keyCode = keyCode;
    this.timePressed = Date.now();
  }

  release() {
    this.timeReleased = Date.now();
  }

  isReleased() {
    return this.timeReleased != undefined;
  }
}

class Word {
  constructor() {
    this.characters = [];
  }

  append(character) {
    this.characters.push(character);
  }
}

function post(path, data) {
  return $.ajax(path, {
    data : JSON.stringify(data),
    contentType : 'application/json',
    type : 'POST',
  });
}

function monitor(selector, onNewWord) {
  var currentWord = new Word();
  var currentChar;

  $(document).ready(() => {
    $(selector).keydown(e => {
      if (e.keyCode === SPACEBAR) {
        return;
      } else {
        if (currentChar && !currentChar.isReleased()) {
          currentChar.release();
          currentWord.append(currentChar);
        }
        currentChar = new Character(e.keyCode);
      }
    });

    $(selector).keyup(e => {
      if (e.keyCode === SPACEBAR) {
        onNewWord(currentWord);
        currentWord = new Word();
      } else if (e.keyCode == currentChar.keyCode) {
        currentChar.release();
        currentWord.append(currentChar);
      }
    });
  });
}
