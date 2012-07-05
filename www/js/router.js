define([
	'app'
], function (app) {
	return Backbone.Router.extend({

		routes: {
			'': 'landing',
			'dashboard': 'dashboard',
			'*path': '404'
		},

		404: function (path) {
			console.log('not found', path);
		},

		landing: function () {
			app.useLayout('landing');
		},

		dashboard: function () {
			app.useLayout('dashboard');
		}

	});
});
