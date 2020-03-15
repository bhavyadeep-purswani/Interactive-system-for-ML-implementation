function loadjscssfile(filename, filetype){
  if (filetype=="js"){
    var fileref=document.createElement('script');
    fileref.setAttribute("type","text/javascript");
    fileref.setAttribute("src", filename);
  }
  else if (filetype=="css"){
    var fileref=document.createElement("link");
    fileref.setAttribute("rel", "stylesheet");
    fileref.setAttribute("type", "text/css");
    fileref.setAttribute("href", filename);
  }
  if (typeof fileref!="undefined")
  document.getElementsByTagName("head")[0].appendChild(fileref);
}
loadjscssfile("js/jquery-3.4.1.min.js", "js");
loadjscssfile("css/bootstrap.min.css", "css");
loadjscssfile("css/commonCssUtils.css", "css");
loadjscssfile("css/fontawesome.css", "css");
loadjscssfile("css/brands.css", "css");
loadjscssfile("css/solid.css", "css");
loadjscssfile("js/CommonJsUtils.js", "js");
setTimeout(() => {
  loadjscssfile("js/popper.min.js", "js");
  loadjscssfile("js/bootstrap.min.js", "js");
  loadjscssfile("js/fontawesome.js", "js");
}, 50);
