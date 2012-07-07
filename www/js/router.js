define([
	'jQuery', 'Underscore', 'app',
	'modules/Dates',
	'modules/Footer',
	'modules/Friends',
	'modules/Header',
	'modules/Notifications',
	'modules/Matchmakers',
	'modules/UserPreview'
], function (
	$, _, app,
	Dates,
	Footer,
	Friends,
	Header,
	Notifications,
	Matchmakers,
	UserPreview
) {
	return Backbone.Router.extend({

		routes: {
			'': 'landing',
			'dashboard': 'dashboard',
			'index-fresh': 'index-fresh',
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
					'.top-matchmakers': new Matchmakers.Views.Top(),
					'.user-preview-medium': new UserPreview.Views.Medium(),
					'.user-preview-small': new UserPreview.Views.Small()
				});
		},
		
		'index-fresh': function () {
			app.useLayout('index-fresh')
				.setViews({
					'.header-top': new Header.Views.Top(),
					'.footer-end': new Footer.Views.End(),

					'.user-preview-medium': new UserPreview.Views.Medium(),

					'.dates-upcoming': new Dates.Views.ListRight(),
					'.friends-list-right': new Friends.Views.ListRight(),
					'.recent-activity': new Notifications.Views.RecentActivity(),
					'.top-matchmakers': new Matchmakers.Views.Top(),				
				});
		}

	});
});
