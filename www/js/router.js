define([
	'app'
], function (app) {
	return Backbone.Router.extend({

		routes: {
			'': 'landing',
			'dashboard': 'dashboard'
		},

		landing: function () {
			if (app.session) {
				app.router.navigate('dashboard');
			} else {
				app.useLayout('landing');
			}
		},

		dashboard: function () {
			app.useLayout('dashboard');
		}

	});
});
