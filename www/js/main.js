define(
['jQuery', 'app', 'router', 'Facebook'],
function ($,  app, Router, Facebook) {

	app.router = new Router();

	Facebook.Event.subscribe('auth.authResponseChange', function (response) {
		console.log('[auth.authResponseChange] The status of the session is: ' + response.status);
		if (response.status === 'connected') {
			Backbone.history.navigate('/dashboard', true);
		}
	});
	Facebook.Event.subscribe('auth.login', function (response) {
		console.log('[auth.login] The status of the session is: ' + response.status);
		// Backbone.history.navigate('/dashboard', true);
	});
	Facebook.init({
		appId      : app.fb_app_id, // App ID
		channelUrl : 'http://freyalove.cofounders.sg/channel.html', // Channel File
		status     : false, // check login status
		cookie     : true, // enable cookies to allow the server to access the session
		xfbml      : false  // parse XFBML
	});
	/*
	Facebook.getLoginStatus(function (response) {
		if (response.status === 'connected') {
			var target = location.href.substr(location.href.indexOf('/', 8));
			if (target === app.root) {
				console.log('REDIRECTING TO DASHBOARD');
				history.replaceState(null, '', '/dashboard');
			}
		}
		Backbone.history.start({
			pushState: true,
			root: app.root
		});
	});
	*/
	Backbone.history.start({
		pushState: true,
		root: app.root
	});

	$(document).on('click', 'a:not([data-bypass])', function (event) {
		var href = $(this).prop('href');
		var root = location.href.substr(0, location.href.indexOf('/', 8)) + app.root;
		if (href && href.slice(0, root.length) === root) {
			event.preventDefault();
			Backbone.history.navigate(href.slice(root.length), true);
		}
	});

});
