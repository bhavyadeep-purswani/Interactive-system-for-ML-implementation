function setCookie(cname, cvalue) {
  document.cookie = cname + "=" + cvalue + ";path=/";
}

function addToSessionStorage(key, value) {
  if (typeof(Storage) !== undefined) {
    sessionStorage.setItem(key, value);
  } else {
    setCookie(key, value);
  }
}
