define(
['jQuery', 'app', 'router', 'Facebook', 'modules/Session/Facebook', 'modules/Stream', 'plugins/backbone.dummysync'],
function ($, app, Router, Facebook, Session, Stream, DummySync) {

	var targetUrl = location.href.substr(location.href.indexOf('/', 8));

	app.router = new Router();
	app.session = new Session();
	app.stream = new Stream();

	DummySync.intercept = app.session.get('dummy');

	app.session
		.on('signIn', function () {
			app.stream.go();
			var url = app.api + 'profile/';
			$.get(url).success(function (response) {
				app.session.save(response);
				Backbone.history.navigate('/dashboard', true);
			});
		})
		.on('signOut', function () {
			app.stream.pause();
			Backbone.history.navigate(app.root, true);
		})
		.on('change:dummy', function () {
			DummySync.intercept = app.session.get('dummy');
		});

	Facebook.init({
		appId: '415866361791508', // App ID
		channelUrl: 'http://freyalove.cofounders.sg/channel.html', // Channel File
		status: false, // check login status
		cookie: true, // enable cookies to allow the server to access the session
		xfbml: false // parse XFBML
	});

	if (app.session.id) {
		app.stream.go();
		if (targetUrl === app.root) {
			history.replaceState(null, '', '/dashboard');
		}
	}

	Backbone.history.start({
		pushState: true,
		root: app.root
	});

	$(document).ajaxError(function (event, request, settings, exception) {
		if (+request.status === 403 && settings.url.indexOf(app.api) !== -1) {
			app.session.signOut();
		}
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
