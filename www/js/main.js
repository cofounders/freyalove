define([
	'jQuery',
	'app',
	'router',
	'plugins/backbone.layoutmanager'
], function ($, app, Router) {

	app.router = new Router();

	Backbone.history.start({
		pushState: true,
		root: app.root
	});

	$(document).on('click', 'a:not([data-bypass])', function (event) {
		var href = $(this).prop('href');
		var root = location.protocol + '//' + location.host + app.root;
		if (href && href.slice(root.length) === root) {
			event.preventDefault();
			Backbone.history.navigate(href.slice(root.length), true);
		}
	});

});
