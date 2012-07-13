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
				Facebook.Event.subscribe('auth.authResponseChange', function (response) {
					console.log('[auth.authResponseChange] The status of the session is: ' + response.status);
					if (response.status === 'connected') {
						Backbone.history.navigate('/dashboard', true);
					}
				});
				Facebook.Event.subscribe('auth.login', function (response) {
					console.log('[auth.login] The status of the session is: ' + response.status);
					Backbone.history.navigate('/dashboard', true);
				});
				Facebook.init({
					appId      : '415866361791508', // App ID
					channelUrl : '//freyalove.cofounders.sg/channel.html', // Channel File
					status     : true, // check login status
					cookie     : true, // enable cookies to allow the server to access the session
					xfbml      : true  // parse XFBML
				});
				Facebook.XFBML.parse();
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
