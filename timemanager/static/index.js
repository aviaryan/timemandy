$(document).ready(function(){
	$('#loginBtn').click(handleLogin);
	$('#registerBtn').click(handleRegister);
});


/*
 * logins the user
 */
function loginUser(email, password){
	$("#loginErrorMessage").text('');
	$.ajax({
		type: 'POST',
		url: '/api/v1/auth/login',
		dataType: 'json',
		data: JSON.stringify({email: email, password: password}),
		contentType: 'application/json',
		success: function(resp){
			console.log(resp['token']);
			// save token as cookie
			setCookie('token', resp['token'], 14)
			// redirect to dashboard page
		},
		error: function(xhr, status, error){
			console.log(xhr.responseJSON['message']);
			$("#loginErrorMessage").text(xhr.responseJSON['message']);
		}
	});
}


function handleLogin(){
	var email = $('#loginEmail').val();
	var password = $('#loginPassword').val();
	console.log(email);
	loginUser(email, password);
}


function handleRegister(){
	var email = $('#registerEmail').val();
	var username = $('#registerUsername').val();
	var password = $('#registerPassword').val();
	console.log(email);
	$("#registerErrorMessage").text('');

	$.ajax({
		type: 'POST',
		url: '/api/v1/users',
		dataType: 'json',
		data: JSON.stringify({email: email, password: password, username: username}),
		contentType: 'application/json',
		success: function(resp){
			console.log(resp);
			// redirect to dashboard page
			loginUser(email, password);
		},
		error: function(xhr, status, error){
			console.log(xhr.responseJSON['message']);
			$("#registerErrorMessage").text(xhr.responseJSON['message']);
		}
	});
}
