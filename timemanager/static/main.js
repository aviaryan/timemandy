// https://www.w3schools.com/js/js_cookies.asp

function setCookie(cname, cvalue, exdays) {
	var d = new Date();
	d.setTime(d.getTime() + (exdays*24*60*60*1000));
	var expires = "expires="+ d.toUTCString();
	document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
	var name = cname + "=";
	var decodedCookie = decodeURIComponent(document.cookie);
	var ca = decodedCookie.split(';');
	for(var i = 0; i <ca.length; i++) {
		var c = ca[i];
		while (c.charAt(0) == ' ') {
			c = c.substring(1);
		}
		if (c.indexOf(name) == 0) {
			return c.substring(name.length, c.length);
		}
	}
	return "";
}

// https://stackoverflow.com/questions/10593013/delete-cookie-by-name
function deleteCookie(name) {
	document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}


function checkLogin(){
	var token = getCookie("token");
	console.log(window.location.pathname);
	if (token !== ""){
		if (window.location.pathname === "/"){
			window.location = '/dashboard';
		}
	} else {
		if (window.location.pathname !== "/"){
			window.location = '/';
		}
	}
}
