var apiIP = "http://147.232.205.10/face";
var faceId = 0;
var answers_count = 0;
var level_count = 1;
var get_next_level_at = 1;
var next_level_at = 1;



function generateRandomNumber(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}

function levelPopup() {
  if (answers_count == get_next_level_at) {
    next_level_at = generateRandomNumber(get_next_level_at + 2, get_next_level_at + 3);
    get_next_level_at += 4;
  }
  else {
    if (answers_count == next_level_at) {
      var level = "#L" + level_count.toString();
      level_count += 1;
      $(level).show().fadeOut(2910);
    } 
  }
  answers_count += 1;
}

// show the instructions before playing
function start(element) {
  element.classList.add("hidden");
  document.getElementById("w").classList.remove("hidden");
  httpGetImgAsync();
}

// get the selected emotion, pass it to server and ask for next face
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

  levelPopup()
}

function parseResponse(responseText) {
  var rt = responseText.replace(/\s/g, '');  // remove spaces
  rt = rt.slice(1, -1); // remove squared brackets
  data = rt.split(','); // split values
  faceId = data[0];
  faceImg = data[1].slice(1, -1); // remove double quotes
      
  var image = document.getElementById("face");
  image.setAttribute("src", faceImg);
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