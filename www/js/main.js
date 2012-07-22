define(
['jQuery', 'app', 'router', 'Facebook', 'modules/Session/Facebook'],
function ($,  app, Router, Facebook, Session) {

	var targetUrl = location.href.substr(location.href.indexOf('/', 8));

	app.router = new Router();
	app.session = new Session();

	Facebook.init({
		appId      : app.fb_app_id, // App ID
		channelUrl : 'http://freyalove.cofounders.sg/channel.html', // Channel File
		status     : false, // check login status
		cookie     : true, // enable cookies to allow the server to access the session
		xfbml      : false  // parse XFBML
	});

	if (app.session.get('id')) {
		if (targetUrl === app.root) {
			history.replaceState(null, '', '/dashboard');
		}
	}

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
