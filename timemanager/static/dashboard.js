$(document).ready(function(){
	checkLogin();
	$('#logoutButton').click(handleLogout);
});

function handleLogout(){
	deleteCookie('token');
	checkLogin();
}
