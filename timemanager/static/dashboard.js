var ractive;
var token;
var allTasks;
var userObj;

$(document).ready(function(){
	checkLogin();
	$('#logoutButton').click(function(){
		deleteCookie('token');
		checkLogin();
	});
	$("#taskSaveBtn").click(handleTaskSave);
	$("#taskUpdateBtn").click(handleTaskUpdate);
	$("#taskDeleteBtn").click(handleTaskDelete);
	token = getCookie('token');
	// set default date
	var today = new Date();
	var formattedDate = today.getFullYear() + '-' + ('0' + (today.getMonth() + 1)).slice(-2) + '-' + ('0' + today.getDate()).slice(-2);
	$("#addDate").val(formattedDate);
	// load data
	loadData();
});


// task new modal

$('#newModal').on('show.bs.modal', function (event) {
	$("#addTaskErrorMessage").text('');
  $("#addUserID").val(userObj.id);
  $("#addUserID").prop('disabled', !userObj.is_admin);
})

// task edit modal

$('#editModal').on('show.bs.modal', function (event) {
	$("#editTaskErrorMessage").text('');
  $("#editUserID").prop('disabled', !userObj.is_admin);
});


function handleTaskSave(){
	var user_id = $("#addUserID").val();
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
			ractive.push('tasks', resp);
		},
		error: function(xhr, status, error){
			console.log(xhr.responseJSON['message']);
			$("#addTaskErrorMessage").text(xhr.responseJSON['message']);
		}
	});
}

function handleTaskUpdate(){
	var user_id = $("#editUserID").val();
	var title = $('#editTitle').val();
	var date = $('#editDate').val() + 'T00:00:00';
	var duration = $('#editDuration').val();
	var comments = $('#editComments').val();
	var id = $("#editID").val();

	var obj = {title: title, date: date, minutes: duration, comments: comments, user_id: user_id};

	$.ajax({
		type: 'PUT',
		url: '/api/v1/tasks/' + id,
		dataType: 'json',
		beforeSend: function(request) {
	    request.setRequestHeader("Authorization", 'Bearer ' + token);
	  },
		data: JSON.stringify(obj),
		contentType: 'application/json',
		success: function(resp){
			console.log(resp);
			$('#editModal').modal('hide'); // hide modal
			// update
			getUserTasks();
		},
		error: function(xhr, status, error){
			console.log(xhr.responseJSON['message']);
			$("#editTaskErrorMessage").text(xhr.responseJSON['message']);
		}
	});
}

function handleTaskDelete(){
	var id = $("#editID").val();

	console.log('task delete');
	$.ajax({
		type: 'DELETE',
		url: '/api/v1/tasks/' + id,
		dataType: 'json',
		beforeSend: function(request) {
	    request.setRequestHeader("Authorization", 'Bearer ' + token);
	  },
		success: function(resp){
			console.log(resp);
			$('#editModal').modal('hide'); // hide modal
			// update
			getUserTasks();
		},
		error: function(xhr, status, error){
			console.log(xhr.responseJSON['message']);
			$("#editTaskErrorMessage").text(xhr.responseJSON['message']);
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

function updateToUserOnlyModeIfNeeded(){
	if (ractive.get('adminTaskFilterText') === 'Show all tasks'){
		tasks = allTasks.filter(function(row){
			return row.user_id == userObj.id;
		});
		ractive.set('tasks', tasks);
	}
}


function handleFilter(){
	var from_ = $("#from_date").val();
	var to = $("#to_date").val();
	getUserTasks(from_, to);
}

function handleFilterClear(){
	$("#from_date").val('');
	$("#to_date").val('');
	getUserTasks();
}


function handleFilterExport(){
	var print_tasks = [];
	var days = {};
	var times = {};

	allTasks.forEach(function(task){
		var date = task.date.replace(/T.*/, '');
		if (date in days){
			days[date].push(task);
			times[date] += task.minutes;
		} else {
			days[date] = [task];
			times[date] = task.minutes;
		}
	});

	for (key in days){
		print_tasks.push({date: key, tasks: days[key], duration: times[key]});
	}
	console.log(print_tasks);

	ractive.set('day_records', print_tasks);

	var mywindow = window.open('', 'Filtered Tasks', 'height=600,width=800');
	var data = $("#print_table")[0].outerHTML;
	mywindow.document.write(data);
}


function taskEdit(event){
	var z = $(event.target);
	var row = z.parent();
	// set to modal
	$('#editUserID').val(row.find('td.task_user_id')[0].textContent);
	$('#editTitle').val(row.find('td.task_title')[0].textContent);
	$('#editDuration').val(row.find('td.task_minutes')[0].textContent);
	$('#editComments').val(row.find('td.task_comments')[0].textContent);
	$('#editDate').val(row.find('td.task_date')[0].textContent);
	$('#editID').val(row.find('td.task_id')[0].textContent);

	// show modal
	$('#editModal').modal('show'); // show modal
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

function getUserTasks(from_date, to_date){
	var qp = '';
	if (from_date !== undefined){
		qp = '&from=' + from_date + '&to=' + to_date;
	}

	$.ajax({
		type: 'GET',
		url: '/api/v1/tasks' + (userObj.is_admin ? '/all' : '') + '?order_by=date.desc' + qp,
		dataType: 'json',
		beforeSend: function(request) {
	    request.setRequestHeader("Authorization", 'Bearer ' + token);
	  },
		success: function(resp){
			console.log(resp);
			allTasks = resp;
			setTaskColors();
			ractive.set('tasks', allTasks);
			updateToUserOnlyModeIfNeeded();
		},
		error: function(xhr, status, error){
			console.log(xhr.responseJSON['message']);
		}
	});
}


function setTaskColors(){
	var matrix = {};
	allTasks.forEach(function(task){
		if (task.user_id !== userObj.id){
			return;
		}
		var date = task.date.replace(/T.*/, '');
		if (date in matrix){
			matrix[date] += task.minutes;
		} else {
			matrix[date] = task.minutes;
		}
	});

	allTasks.forEach(function(task, index){
		if (task.user_id !== userObj.id){
			return;
		}
		var date = task.date.replace(/T.*/, '');
		if (matrix[date] >= userObj.pref_wh * 60){
			allTasks[index]['color_green'] = true;
		} else {
			allTasks[index]['color_red'] = true;
		}
	});
}
