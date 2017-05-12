const SPACEBAR = 32;
const ENTER = 13;
const BACKSPACE = 8;

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

function isBreak(keyCode) {
  return e.keyCode === SPACEBAR || e.keyCode === ENTER || e.keyCode === BACKSPACE;
}

function monitor(selector, onNewWord) {
  var currentWord = new Word();
  var currentChar;

  $(document).ready(() => {
    $(selector).keydown(e => {
      if (isBreak(e.keyCode)) {
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
      if (isBreak(e.keyCode)) {
        onNewWord(currentWord);
        currentWord = new Word();
      } else if (e.keyCode == currentChar.keyCode) {
        currentChar.release();
        currentWord.append(currentChar);
      }
    });
  });
}
