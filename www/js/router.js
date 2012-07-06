define([
	'jQuery', 'Underscore', 'app',
	'modules/Header',
	'modules/Footer'
], function (
	$, _, app,
	Header,
	Footer
) {
	return Backbone.Router.extend({

		routes: {
			'': 'landing',
			'dashboard': 'dashboard',
			'*path': '404'
		},

		404: function (path) {
			app.useLayout('404');
		},

		landing: function () {
			app.useLayout('landing');
		},

		dashboard: function () {
			app.useLayout('dashboard')
				.setViews({
					'.partial.header': new Header.Views.Top(),
					'.partial.footer': new Footer.Views.End()
				});
		}

	});
});
