define([
	'jQuery', 'Underscore', 'Backbone', 'app',
	'modules/Dates',
	'modules/Footer',
	'modules/Friends',
	'modules/Header',
	'modules/Notifications',
	'modules/Matchmakers',
	'modules/UserPreview'
], function (
	$, _, Backbone, app,
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
			'fresh': 'fresh',
			'dashboard': 'dashboard',
			'inbox': 'inbox',
			'logout': 'logout',
			'matchmake': 'matchmake',
			'matchmakers': 'matchmakers',
			'message': 'message',
			'profile': 'profile',
			'*path': '404'
		},

		// Handlers

		404: function (path) {
			app.useLayout('404');
		},

		landing: function () {
			app.useLayout('landing');
			require(['Facebook'], function (Facebook) {
				Facebook.XFBML.parse();
			});
		},

		logout: function () {
			console.log('LOGGING OUT');
			require(['Facebook'], function (Facebook) {
				console.log('Facebook before logout');
				Facebook.logout(function (response) {
					console.log('Facebook logout callback');
				});
				console.log('Facebook after logout');
				Backbone.history.navigate('', true);
			});
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

		inbox: function () {
			app.useLayout('inbox')
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

		logout: function () {
			require(['Facebook'], function (Facebook) {
				Facebook.logout(function (response) {
					console.log('Facebook logout callback');
				});
				Backbone.history.navigate('', true);
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

		message: function () {
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
		},

		profile: function () {
			app.useLayout('profile')
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
