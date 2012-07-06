define([
	'jQuery', 'Underscore', 'app',
	'modules/Header',
	'modules/Footer',
	'modules/Friends',
	'modules/Notifications',
	'modules/Matchmakers'
], function (
	$, _, app,
	Header,
	Footer,
	Friends,
	Notifications,
	Matchmakers
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
					'.header-top': new Header.Views.Top(),
					'.footer-end': new Footer.Views.End(),
					'.friends-list-right': new Friends.Views.ListRight(),
					'.recent-activity': new Notifications.Views.RecentActivity(),
					'.top-matchmakers': new Matchmakers.Views.Top()
				});
		}

	});
});
