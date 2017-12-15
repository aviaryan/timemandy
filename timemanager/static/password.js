var ractive;
var token;
var userID;


$(document).ready(function(){
	checkLogin();
	$('#logoutButton').click(function(){
		window.location.href = '/logout';
	});

	token = getCookie('token');
	// load data
	loadData();
});


function loadData(){
	userID = window.location.href.substr(window.location.href.lastIndexOf('/') + 1);
	console.log(userID);
	ractive = new Ractive({
	  target: '#target',
	  template: '#template',
	  data: {
	  	userID: userID,
	  	password: ''
	  }
	});
}


function showMessage(message){
	$("#errorMessage").text(message);
	setTimeout(function(){
		$("#errorMessage").text('');
	}, 3000);
}


function handleSave(){
	var password = ractive.get('password');
	console.log(password);

	$.ajax({
		type: 'PUT',
		url: '/api/v1/users/' + ractive.get('userID'),
		dataType: 'json',
		beforeSend: function(request) {
	    request.setRequestHeader("Authorization", 'Bearer ' + token);
	  },
		data: JSON.stringify({password: password}),
		contentType: 'application/json',
		success: function(resp){
			console.log(resp);
			showMessage('Password updated successfully');
		},
		error: function(xhr, status, error){
			console.log(xhr.responseJSON['message']);
			showMessage(xhr.responseJSON['message']);
		}
	});
}
