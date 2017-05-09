class Character {
  constructor(keyCode) {
    this.keyCode = keyCode;
    this.timePressed = Date.now();
  }

  release() {
    this.timeReleased = Date.now();
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

const SPACEBAR = 32;

let words = [];
var currentWord = new Word();
var currentChar;

$(document).ready(() => {
  $('#editarea').keydown(e => {
    if (e.keyCode === SPACEBAR) {
      return;
    } else {
      currentChar = new Character(e.keyCode);
    }
  });

  $('#editarea').keyup(e => {
    if (e.keyCode === SPACEBAR) {
      words.push(currentWord);
      currentWord = new Word();
    } else {
      currentChar.release();
      currentWord.append(currentChar);
    }
  });
});
