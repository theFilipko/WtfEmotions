var faceId = 0;
var apiIP = "http://147.232.205.10/face";

function start(element) {
  element.classList.add("hidden");
  document.getElementById("w").classList.remove("hidden");
  httpGetImgAsync();
}

function proceedAsync(emotion) {
  if (faceId == 0)
    return;
  
  var data = {};
  data.id = faceId;
  data.emotion = emotion;
  var json = JSON.stringify(data);

  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("PUT", apiIP, true);
  xmlHttp.onload = function() {
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
      parseResponse(this.responseText);
  };
  xmlHttp.send(json)
}

function parseResponse(responseText) {
  var rt = responseText.replace(/\s/g, '');  // remove spaces
  rt = rt.slice(1, -1); // remove squared brackets
  data = rt.split(','); // split values
  faceId = data[0];
  faceImg = data[1].slice(1, -1); // remove double quotes
      
  var image = document.getElementById("face");
  image.setAttribute("src", faceImg);
  // document.getElementById("xxx").innerHTML = "_" + faceId + "_" + faceImg + "_";
  // document.getElementById("xxx").innerHTML = "_" + responseText + "_";
  // console.log(xmlHttp.responseText);
  // callback(xmlHttp.responseText);
}

// Send a 'GET' request to the specified url and run the callback function when it completes.
function httpGetImgAsync() {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function() {
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
      parseResponse(this.responseText); 
  };

  xmlHttp.open("GET", apiIP, true);
  // xmlHttp.setRequestHeader("Access-Control-Allow-Origin", "*");
  xmlHttp.send(null);
}

function httpPutEmotionAsync(emotion) {
  var data = {};
  data.id = faceId;
  data.emotion = emotion;
  var json = JSON.stringify(data);

  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onload = function() {
    document.getElementById("xxx").innerHTML = "_" + this.responseText + "_";
  };
  xmlHttp.open("PUT", apiIP, true);
  xmlHttp.send(json)
}

function proceed(emotion) {
  httpPutEmotionAsync(emotion);
  httpGetImgAsync();
}

function httpGetImgSync() {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function() {
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
      var responseText = this.responseText.replace(/\s/g, '');  // remove spaces
      responseText = responseText.slice(1, -1); // remove squared brackets
      response = responseText.split(','); // split values
      faceId = response[0];
      faceImg = response[1].slice(1, -1); // remove double quotes
      var image = document.getElementById("face");
      image.setAttribute("src", faceImg);
    }      
  };

  xmlHttp.open("GET", apiIP, false);
  xmlHttp.send(null);
}

function httpPutEmotionSync(emotion) {
  var data = {};
  data.id = faceId;
  data.emotion = emotion;
  var json = JSON.stringify(data);

  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("PUT", apiIP, false);
  xmlHttp.send(json)
}