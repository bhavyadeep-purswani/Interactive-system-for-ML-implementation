    
    
//To set link of navbar
//document.getElementById("navHome").setAttribute("href","");
//document.getElementById("navDataset").setAttribute("href","");


    $("#menu-toggle").click(function(e) {
      e.preventDefault();
      $("#wrapper").toggleClass("toggled");
    });
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

function createFileHead(data,metaData,type,div)
{
if(type=="check")
{
createTableCheck(data,metaData,div)
}
else if(type=="radio")
{
createTableRadio(data,metaData,div)
}
else{
createTableNormal(data,metaData,div)
}
}

function createTableRadio(data,metaData,div)
  {
    console.log(div)
    var tbl=document.createElement('table');
   
   div.innerHTML="";
    tbl.style.width = '100%';
    tbl.setAttribute('border', '1');
    var tbdy = document.createElement('tbody');
    var tr = document.createElement('tr');
    for (var j = 0; j < metaData.length; j++)
    {
      var td = document.createElement('td');

      td.appendChild(document.createTextNode(metaData[j]));
      var input= document.createElement('input');
          input.setAttribute('type','radio');
          input.setAttribute('name','targetColumn');
          input.setAttribute('value',metaData[j]);
          td.appendChild(input);
      tr.appendChild(td);
    }

    tbdy.appendChild(tr);
    for (var i = 0; i < 5;i++)
    {
      var tr = document.createElement('tr');
      for (var j = 0; j < metaData.length; j++)
      {
        var td = document.createElement('td');
        td.appendChild(document.createTextNode(data[i][j]));
        tr.appendChild(td)
      }
      tbdy.appendChild(tr);
    }
    tbl.appendChild(tbdy);
  div.appendChild(tbl)
  }
  function createTableCheck(data,metaData,div)
  {
    
    var tbl=document.createElement('table');
    
   div.innerHTML="";
    tbl.style.width = '100%';
    tbl.setAttribute('border', '1');
    var tbdy = document.createElement('tbody');
    var tr = document.createElement('tr');
    for (var j = 0; j < metaData.length; j++)
    {
      var td = document.createElement('td');

      td.appendChild(document.createTextNode(metaData[j]));
      var input= document.createElement('input');
          input.setAttribute('type','checkbox');
          input.setAttribute('name','removeColumns[]');
          input.setAttribute('value',metaData[j]);
          td.appendChild(input);
          tr.appendChild(td);
    }

    tbdy.appendChild(tr);
    for (var i = 0; i < 5;i++)
    {
      var tr = document.createElement('tr');
      for (var j = 0; j < metaData.length; j++)
      {
        var td = document.createElement('td');
        td.appendChild(document.createTextNode(data[i][j]));
        tr.appendChild(td)
      }
      tbdy.appendChild(tr);
    }
    tbl.appendChild(tbdy);
   
   div.appendChild(tbl);
  }
  function createTableNormal(data,metaData,div)
  {
    
    var tbl=document.createElement('table');
    
   div.innerHTML="";
    tbl.style.width = '100%';
    tbl.setAttribute('border', '1');
    var tbdy = document.createElement('tbody');
    var tr = document.createElement('tr');
    for (var j = 0; j < metaData.length; j++)
    {
      var td = document.createElement('td');

      td.appendChild(document.createTextNode(metaData[j]));
      
          tr.appendChild(td);
    }

    tbdy.appendChild(tr);
    for (var i = 0; i < 5;i++)
    {
      var tr = document.createElement('tr');
      for (var j = 0; j < metaData.length; j++)
      {
        var td = document.createElement('td');
        td.appendChild(document.createTextNode(data[i][j]));
        tr.appendChild(td)
      }
      tbdy.appendChild(tr);
    }
    tbl.appendChild(tbdy);

   
   div.appendChild(tbl);
  }

  