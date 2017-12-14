var ractive;
var token;
var allTasks;
var userObj;

$(document).ready(function(){
	checkLogin();
	$('#logoutButton').click(handleLogout);
	$("#taskSaveBtn").click(handleTaskSave);
	token = getCookie('token');
	// set default date
	var today = new Date();
	var formattedDate = today.getFullYear() + '-' + ('0' + (today.getMonth() + 1)).slice(-2) + '-' + ('0' + today.getDate()).slice(-2);
	$("#addDate").val(formattedDate);
	// load data
	loadData();
});

function handleLogout(){
	deleteCookie('token');
	checkLogin();
}


// task new modal

$('#newModal').on('show.bs.modal', function (event) {
	$("#addTaskErrorMessage").text('');
  $("#addUserID").val(userObj.id);
  $("#addUserID").prop('disabled', !userObj.is_admin);
})


function handleTaskSave(){
	var user_id = $("addUserID").val();
	var title = $('#addTitle').val();
	var date = $('#addDate').val() + 'T00:00:00';
	var duration = $('#addDuration').val();
	var comments = $('#addComments').val();
	console.log(title + date);

	var obj = {title: title, date: date, minutes: duration, comments: comments, user_id: user_id};

	$.ajax({
		type: 'POST',
		url: '/api/v1/tasks',
		dataType: 'json',
		beforeSend: function(request) {
	    request.setRequestHeader("Authorization", 'Bearer ' + token);
	  },
		data: JSON.stringify(obj),
		contentType: 'application/json',
		success: function(resp){
			console.log(resp);
			$('#newModal').modal('hide'); // hide modal
			ractive.push('tasks', obj);
		},
		error: function(xhr, status, error){
			console.log(xhr.responseJSON['message']);
			$("#addTaskErrorMessage").text(xhr.responseJSON['message']);
		}
	});
}

// admin switch

function handleAdminSwitch(){
	if (ractive.get('adminTaskFilterText') === 'Show only mine'){
		ractive.set('adminTaskFilterText', 'Show all tasks');
		tasks = allTasks.filter(function(row){
			return row.user_id == userObj.id;
		});
		ractive.set('tasks', tasks);
	} else {
		ractive.set('adminTaskFilterText', 'Show only mine');
		ractive.set('tasks', allTasks);
	}
}

function loadData(){
	ractive = new Ractive({
	  target: '#target',
	  template: '#template',
	  data: { name: 'User', adminTaskFilterText: 'Show only mine' }
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
			allTasks = resp;
			ractive.set('tasks', resp);
		},
		error: function(xhr, status, error){
			console.log(xhr.responseJSON['message']);
		}
	});
}
