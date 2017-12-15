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
	  	active_user: {}
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
			ractive.set('active_user', userObj);
			// hide button
			if (!(userObj.is_admin || userObj.is_manager)){
				$("#all_users_btn").hide();
			}
			// load users
			getUsers();
		},
		error: function(xhr, status, error){
			console.log(xhr.responseJSON['message']);
		}
	});
}

function getUsers(){
	$.ajax({
		type: 'GET',
		url: '/api/v1/users',
		dataType: 'json',
		beforeSend: function(request) {
	    request.setRequestHeader("Authorization", 'Bearer ' + token);
	  },
		success: function(resp){
			console.log(resp);
			// allTasks = resp;
			// setTaskColors();
			ractive.set('users', resp);
			// updateToUserOnlyModeIfNeeded();
		},
		error: function(xhr, status, error){
			console.log(xhr.responseJSON['message']);
		}
	});
}


function userEdit(event){
	var z = $(event.target);
	var row = z.parent();
	// set to modal
	var userID = row.find('td.user_id')[0].textContent;
	console.log(userID);
	launchEditBox(userID);
}


function launchEditBox(userID){
	$.ajax({
		type: 'GET',
		url: '/api/v1/users/' + userID,
		dataType: 'json',
		beforeSend: function(request) {
	    request.setRequestHeader("Authorization", 'Bearer ' + token);
	  },
		success: function(resp){
			ractive.set('edit_user', resp);
			// show modal
			$('#editModal').modal('show');
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


function showNewMessage(message){
	$("#newErrorMessage").text(message);
	setTimeout(function(){
		$("#newErrorMessage").text('');
	}, 3000);
}

function updateUser(){
	var user = ractive.get('edit_user');
	console.log(user);

	$.ajax({
		type: 'PUT',
		url: '/api/v1/users/' + user.id,
		dataType: 'json',
		beforeSend: function(request) {
	    request.setRequestHeader("Authorization", 'Bearer ' + token);
	  },
		data: JSON.stringify(user),
		contentType: 'application/json',
		success: function(resp){
			console.log(resp);
			$('#editModal').modal('hide'); // hide modal
			getUsers();  // refresh
		},
		error: function(xhr, status, error){
			console.log(xhr.responseJSON['message']);
			showMessage(xhr.responseJSON['message']);
		}
	});
}


function deleteUser(){
	var user = ractive.get('edit_user');
	console.log(user);

	$.ajax({
		type: 'DELETE',
		url: '/api/v1/users/' + user.id,
		dataType: 'json',
		beforeSend: function(request) {
	    request.setRequestHeader("Authorization", 'Bearer ' + token);
	  },
		success: function(resp){
			console.log(resp);
			$('#editModal').modal('hide'); // hide modal
			if (user.id === userObj.id){ // deleted themselves
				$("#logoutButton").click();
			}
			getUsers();  // refresh
		},
		error: function(xhr, status, error){
			console.log(xhr.responseJSON['message']);
			$("#editTaskErrorMessage").text(xhr.responseJSON['message']);
		}
	});
}


function createUser(){
	var user = ractive.get('new_user');
	console.log(user);

	$.ajax({
		type: 'POST',
		url: '/api/v1/users',
		dataType: 'json',
		beforeSend: function(request) {
	    request.setRequestHeader("Authorization", 'Bearer ' + token);
	  },
		data: JSON.stringify(user),
		contentType: 'application/json',
		success: function(resp){
			console.log(resp);
			$('#newModal').modal('hide'); // hide modal
			getUsers();  // refresh
		},
		error: function(xhr, status, error){
			console.log(xhr.responseJSON['message']);
			showNewMessage(xhr.responseJSON['message']);
		}
	});
}
