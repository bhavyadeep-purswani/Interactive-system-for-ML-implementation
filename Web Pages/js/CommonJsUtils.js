    
    
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

function getFromSessionStorage(key) {
  if (typeof(Storage) !== undefined) {
    return localStorage.getItem(key);
  } else {
    return getCookie(key);
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

  