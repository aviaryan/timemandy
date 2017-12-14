var ractive;
var token;
var userObj;


$(document).ready(function(){
	checkLogin();
	$('#logoutButton').click(function(){
		deleteCookie('token');
		checkLogin();
	});

	token = getCookie('token');
	// load data
	loadData();
});



function loadData(){
	ractive = new Ractive({
	  target: '#target',
	  template: '#template',
	  data: {
	  	user: {
	  		// add
	  	}
	  }
	});
	// ractive loaded
	// load user data
	getUserInfo();
}


function getUserInfo(){
	$.ajax({
		type: 'GET',
		url: '/api/v1/users/user',
		dataType: 'json',
		beforeSend: function(request) {
	    request.setRequestHeader("Authorization", 'Bearer ' + token);
	  },
		success: function(resp){
			userObj = resp;
			ractive.set('user', userObj);
			ractive.set('oldUser', userObj); // not live updated
		},
		error: function(xhr, status, error){
			console.log(xhr.responseJSON['message']);
		}
	});
}


function handleSave(){
	var user = ractive.get('user');
	console.log(user);

	$.ajax({
		type: 'PUT',
		url: '/api/v1/users/' + userObj.id,
		dataType: 'json',
		beforeSend: function(request) {
	    request.setRequestHeader("Authorization", 'Bearer ' + token);
	  },
		data: JSON.stringify(user),
		contentType: 'application/json',
		success: function(resp){
			console.log(resp);
			ractive.set('oldUser', userObj); // not live updated
		},
		error: function(xhr, status, error){
			console.log(xhr.responseJSON['message']);
			$("#errorMessage").text(xhr.responseJSON['message']);
		}
	});
}
