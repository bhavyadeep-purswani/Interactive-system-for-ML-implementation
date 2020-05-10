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

function getFromSessionStorage(key, defaultValue) {
  if (typeof(Storage) !== undefined) {
    return localStorage.getItem(key) == null ? defaultValue : localStorage.getItem(key);
  } else {
    return getCookie(key) == null ? defaultValue : getCookie(key);
  }
}

function getBool(boolean) {
  if (boolean == "True" || boolean == true || boolean == "true") {
    return true;
  } else {
    return false;
  }
}

function showLoading(show) {
  if (show) {
    document.getElementById("cover-spin").style.display = "block";
  } else {
    document.getElementById("cover-spin").style.display = "none";
  }
}

function makeRequest(url, formData, method, callback) {
  var xhr = new XMLHttpRequest();
  xhr.open(method, url, true);
  var retryAttempts = 0;
  xhr.onreadystatechange = function ()
  {
    if (xhr.readyState === 4)
    {
      if (xhr.status === 200) {
        callback(xhr.responseText);
      } else {
        if (retryAttempts < 5) {
          xhr.open(method, url, true);
          if (method == "GET" || method == "get" || formData == null) {
            xhr.send();
          } else {
            xhr.send(formData);
          }
          retryAttempts += 1;
        }
      }
    }
  };
  if (method == "GET" || method == "get" || formData == null) {
    xhr.send();
  } else {
    xhr.send(formData);
  }
}

function makeDownloadRequest(url, formData, method) {
  var xhr = new XMLHttpRequest();
  xhr.open(method, url, true);
  xhr.responseType = 'blob';
  var retryAttempts = 0;
  xhr.onreadystatechange = function ()
  {
    if (xhr.readyState === 4)
    {
      if (xhr.status === 200) {
        var blob = xhr.response;
        var fileName = "predictions.csv";
        saveBlob(blob, fileName);
      } else {
        if (retryAttempts < 5) {
          xhr.open(method, url, true);
          if (method == "GET" || method == "get" || formData == null) {
            xhr.send();
          } else {
            xhr.send(formData);
          }
          retryAttempts += 1;
        }
      }
    }
  };
  if (method == "GET" || method == "get" || formData == null) {
    xhr.send();
  } else {
    xhr.send(formData);
  }
}

function saveBlob(blob, fileName) {
    var a = document.createElement('a');
    a.href = window.URL.createObjectURL(blob);
    a.download = fileName;
    a.dispatchEvent(new MouseEvent('click'));
}

function getStrFromBool(bool) {
  if (bool) {
    return "True";
  } else {
    return "False";
  }
}

function showObject(object) {
  object.style.display = "block";
}

function hideObject(object) {
  object.style.display = "none";
}
