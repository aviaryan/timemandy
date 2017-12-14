var ractive;
var token;
var userObj;

$(document).ready(function(){
	checkLogin();
	$('#logoutButton').click(handleLogout);
	token = getCookie('token');
	// load data
	loadData();
});

function handleLogout(){
	deleteCookie('token');
	checkLogin();
}

function loadData(){
	ractive = new Ractive({
	  target: '#target',
	  template: '#template',
	  data: { name: 'User' }
	});

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
			var name = resp['fullname'] || resp['username'];
			ractive.set('name', name);
			ractive.set('isAdmin', userObj.is_admin);
			// hide button
			if (!(userObj.is_admin || userObj.is_manager)){
				$("#all_users_btn").hide();
			}
			// waited for user id
			getUserTasks();
		},
		error: function(xhr, status, error){
			console.log(xhr.responseJSON['message']);
		}
	});
}

function getUserTasks(){
	$.ajax({
		type: 'GET',
		url: '/api/v1/tasks' + (userObj.is_admin ? '/all' : ''),
		dataType: 'json',
		beforeSend: function(request) {
	    request.setRequestHeader("Authorization", 'Bearer ' + token);
	  },
		success: function(resp){
			console.log(resp);
			ractive.set('tasks', resp);
		},
		error: function(xhr, status, error){
			console.log(xhr.responseJSON['message']);
		}
	});
}
