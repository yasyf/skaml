function evaluate(username, password, delays) {
  if (password.length - 1 != delays.length) {
    throw "invalid delays length";
  }

  Node.prototype.fire = function(type, options) {
    let event = new CustomEvent(type);
    for (var p in options)
      event[p] = options[p];
    this.dispatchEvent(event);
  };

  let usernameElt = document.getElementById("username");
  let passwordElt = document.getElementById("password");
  let submitElt   = document.getElementsByTagName('button')[0];

  usernameElt.value = username;

  function nextChar(i) {
    let char = password[i];
    passwordElt.value += char;
    passwordElt.fire("keypress", {keyCode: char.charCodeAt(0)});
    if (i < password.length - 1) {
      setTimeout(nextChar, delays[i], i + 1);
    } else {
      submitElt.click();
    }
  }

  nextChar(0);
}
