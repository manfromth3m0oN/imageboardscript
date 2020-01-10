function doSubmit(){
	var formData = new FormData();

	var fileSelect = document.getElementById("image");
	if(fileSelect.files && fileSelect.files.length == 1){
		var file = fileSelect.files[0]
		formData.set("file", file , file.name);
	}

	var name = document.getElementById("name");
	formData.set("name", name.value)
	var body = document.getElementById("body");
	formData.set("body", body.value)
	var board = $("#board").text()
	formData.set("board", board)

	// Http Request
	var request = new XMLHttpRequest();
	request.open('POST', "/post");
	request.send(formData);
}
