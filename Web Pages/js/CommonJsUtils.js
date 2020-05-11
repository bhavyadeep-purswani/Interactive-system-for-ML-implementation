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
        } else {
          //show error occured
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

function showFullDataset() {
  var body = document.getElementsByTagName("body")[0];
  var child = document.createElement("div");
  child.setAttribute("include-html", "fullDataModel.html");
  body.appendChild(child);
  includeHTML();
  showLoading(true);
  var url = "http://127.0.0.1:5000/trainData";
  var callback = function(response) {
    var json = JSON.parse(response);
    var data=json.data;
    var metadata=json.metaData;
    createTableCheckboxFullData(data,metadata);
    document.getElementById("showFullDataBtn").click();
    showLoading(false);
  };
  makeRequest(url, null, "GET", callback);
}

function createTableCheckboxFullData(data,metaData)
{
  var tbl=document.createElement('table');
  var tblDiv = document.getElementById("tableDivFullData");
  tblDiv.innerHTML="";
  tbl.style.width = '100%';
  tbl.setAttribute('class', 'table table-bordered table-striped');
  tblDiv.setAttribute('style', "overflow-x:auto; max-height: 500px; overflow-y:auto;");
  var thead = document.createElement('thead');
  var tbdy = document.createElement('tbody');
  var tr = document.createElement('tr');
  for (var j = 0; j < metaData.length; j++)
  {
    var th = document.createElement('th');
    th.appendChild(document.createTextNode(metaData[j] + " "));
    if (metaData[j] != "Target") {
      var input= document.createElement('input');
      input.setAttribute('type','checkbox');
      input.setAttribute('name','columnsDeleteFullData[]');
      input.setAttribute('value',metaData[j]);
      input.setAttribute('style',"display:inline;");
      th.appendChild(input);
    }
    tr.appendChild(th);
  }
  thead.appendChild(tr);
  tbl.appendChild(thead);
  for (var i = 0; i < data.length;i++)
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
  tblDiv.appendChild(tbl);
}

function deleteColumnsFromFullData() {
  var checkedValue = [];
  var inputElements = document.getElementsByName('columnsDeleteFullData[]');
  for(var i=0; inputElements[i]; i++){
        if(inputElements[i].checked){
             checkedValue.push(inputElements[i].value);
        }
  }
  if (checkedValue.length != 0) {
    var url = "http://127.0.0.1:5000/removeColumns";
    var form_data = new FormData();
    var callback = function(response) {
      location.reload();
    };
    form_data.append("removeColumns", checkedValue.join(","));
    makeRequest(url, form_data, "POST", callback);
  } else {
    document.getElementById("closeModal").click();
  }
}

function includeHTML() {
  var z, i, elmnt, file, xhttp;
  z = document.getElementsByTagName("*");
  for (i = 0; i < z.length; i++) {
    elmnt = z[i];
    file = elmnt.getAttribute("include-html");
    if (file) {
      elmnt.innerHTML = `<button type="button" style="display:none;" id = "showFullDataBtn" data-toggle="modal" data-target="#fullData">Full Data Model</button>
      <div class="modal fade" id="fullData" tabindex="-1" role="dialog" aria-labelledby="fullDataLabel" aria-hidden="true">
        <div class="modal-dialog modal-xl" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="fullDataLabel">Train Dataset</h5>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body" id = "fullDataBody">
            <div id = "dataHeadFullData">
              <div id = "tableDivFullData">
              </div>
            </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" id = "closeModal" data-dismiss="modal">Close</button>
              <button type="button" class="btn btn-danger" onclick = "deleteColumnsFromFullData();">Delete Columns</button>
            </div>
          </div>
        </div>
      </div>`;
      elmnt.removeAttribute("include-html");
      includeHTML();
      return;
    }
  }

  function deleteColumnsFromFullData() {
    var checkedValue = [];
    var inputElements = document.getElementsByName('columnsDeleteFullData[]');
    for(var i=0; inputElements[i]; i++){
          if(inputElements[i].checked){
               checkedValue.push(inputElements[i].value);
          }
    }
    if (checkedValue.length != 0) {
      var url = "http://127.0.0.1:5000/removeColumns";
      var form_data = new FormData();
      var callback = function(response) {
        location.reload();
      };
      form_data.append("removeColumns", checkedValue.join(","));
      makeRequest(url, form_data, "POST", labelEncodeColumns);
    } else {
      document.getElementById("closeModal").click();
    }
  }
}
