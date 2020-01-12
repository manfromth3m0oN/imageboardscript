function doSubmit() {
  var formData = new FormData();

  var fileSelect = document.getElementById("image");
  if (fileSelect.files && fileSelect.files.length == 1) {
    var file = fileSelect.files[0];
    formData.set("file", file, file.name);
  }

  var name = document.getElementById("name");
  formData.set("name", name.value);
  var body = document.getElementById("body");
  formData.set("body", body.value);
  if (window.location.href.split("/").length > 4){
    var url = window.location.href.split("/")
    formData.set("replyingto", url[url.length - 1])
  }
  var board = $("#board").text();
  formData.set("board", board);

  // Http Request
  var request = new XMLHttpRequest();
  request.open("POST", "/post");
  request.send(formData);
  location.reload(true);
}

function boardSubmit() {
  var formData = new FormData();

  var boardName = document.getElementById("newboard-name");
  formData.set("boardName", boardName.value);
  var boardShortName = document.getElementById("newboard-shortname")
  formData.set("boardShortName", boardShortName.value);
  
  var request = new XMLHttpRequest();
  var responce = ""
  request.onreadystatechange = function() {
    if (request.readyState == XMLHttpRequest.DONE) {
        var responce = request.responseText
    }
  }
  request.open("POST", "/boardsubmit")
  request.send(formData)
  if (responce.substring(0,3) == 'ERR'){
    document.getElementById('status').innerHTML = "<p>",responce,'</p>';
  }
}
