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

		// Paths

		routes: {
			'': 'landing',
			'dashboard': 'dashboard',
			'fresh': 'fresh',
			'matchmake': 'matchmake',
			'matchmakers': 'matchmakers',
			'message-list': 'message-list',
			'message': 'message',
			'*path': '404'
		},

		// Handlers

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

		fresh: function () {
			app.useLayout('fresh')
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
		matchmake: function () {
			app.useLayout('matchmake')
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
		matchmakers: function () {
			app.useLayout('matchmakers')
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
		'message-list': function () {
			app.useLayout('message-list')
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
		'message': function () {
			app.useLayout('message')
				.setViews({
					'.header-top': new Header.Views.Top(),
					'.footer-end': new Footer.Views.End(),
					'.friends-list-right': new Friends.Views.ListRight(),
					'.recent-activity': new Notifications.Views.RecentActivity(),
					'.top-matchmakers': new Matchmakers.Views.Top(),
					'.user-preview-medium': new UserPreview.Views.Medium(),
					'.user-preview-small': new UserPreview.Views.Small()				
				});
		}

	});
});
