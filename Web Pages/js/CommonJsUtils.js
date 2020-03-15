function setCookie(cname, cvalue) {
  document.cookie = cname + "=" + cvalue + ";path=/";
}

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return null;
}

function addToSessionStorage(key, value) {
  if (typeof(Storage) !== undefined) {
    localStorage.setItem(key, value);
  } else {
    setCookie(key, value);
  }
}

function getFromSessionStorage(key) {
  if (typeof(Storage) !== undefined) {
    return localStorage.getItem(key);
  } else {
    return getCookie(key);
  }
}
