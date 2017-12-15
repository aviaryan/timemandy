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
			// hide button
			if (!(userObj.is_admin || userObj.is_manager)){
				$("#all_users_btn").hide();
			}
		},
		error: function(xhr, status, error){
			console.log(xhr.responseJSON['message']);
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
			showMessage('Updated successfully');
		},
		error: function(xhr, status, error){
			console.log(xhr.responseJSON['message']);
			showMessage(xhr.responseJSON['message']);
		}
	});
}


function handleDelete(){
	$.ajax({
		type: 'DELETE',
		url: '/api/v1/users/' + userObj.id,
		dataType: 'json',
		beforeSend: function(request) {
	    request.setRequestHeader("Authorization", 'Bearer ' + token);
	  },
		success: function(resp){
			console.log(resp);
			showMessage('User deleted');
			$("#logoutButton").click();
		},
		error: function(xhr, status, error){
			console.log(xhr.responseJSON['message']);
			$("#editTaskErrorMessage").text(xhr.responseJSON['message']);
		}
	});
}
