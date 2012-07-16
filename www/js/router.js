define([
	'jQuery', 'Underscore', 'Backbone', 'app',
	'modules/Dates',
	'modules/Footer',
	'modules/Friends',
	'modules/Header',
	'modules/Notifications',
	'modules/Leaderboard',
	'modules/UserPreview'
], function (
	$, _, Backbone, app,
	Dates,
	Footer,
	Friends,
	Header,
	Notifications,
	Leaderboard,
	UserPreview
) {
	return Backbone.Router.extend({

		// Paths

		routes: {
			'': 'landing',
			'about': 'about',
			'dashboard': 'dashboard',
			'faq': 'faq',
 			'fresh': 'fresh', // TODO: merge into dashboard
			'inbox': 'inbox',
			'logout': 'logout',
			'matchmake': 'matchmake',
			'Leaderboard': 'Leaderboard',
			'message': 'message',
			'profile': 'profile', // TODO: merge fof and friends into this
			'terms': 'terms',
			'*path': '404'
		},

		// Handlers

		404: function (path) {
			app.useLayout('404')
				.setViews({
					'.header-top': new Header.Views.Top(),
					'.footer-end': new Footer.Views.End(),
				}).render();
		},

		about: function (path) {
			app.useLayout('about')
				.setViews({
					'.header-top': new Header.Views.Top(),
					'.footer-end': new Footer.Views.End(),
				}).render();
		},

		landing: function () {
			app.useLayout('landing')
				.setViews({
					'.footer-end': new Footer.Views.End()
				}).render();
		},

		logout: function () {
			require(['Facebook'], function (Facebook) {
				Facebook.logout(function (response) {
				});
				Backbone.history.navigate('', true);
			});
		},

		dashboard: function () {
			app.useLayout('dashboard')
				.setViews({
					'.header-top': new Header.Views.Top(),
					'.footer-end': new Footer.Views.End(),
					'.dates-upcoming': new Friends.Views.UpcomingDates(),
					'.friends-list-right': new Friends.Views.ListRight(),
					'.recent-activity': new Notifications.Views.RecentActivity(),
					'.top-leaderboard': new Leaderboard.Views.Top(),
					'.user-preview-medium': new UserPreview.Views.Medium(),
					'.user-preview-small': new UserPreview.Views.Small()
				}).render();
		},
		
		faq: function (path) {
			app.useLayout('faq')
				.setViews({
					'.header-top': new Header.Views.Top(),
					'.footer-end': new Footer.Views.End(),
				});
		},

		fresh: function () { /* TODO: merge into dashboard */
			app.useLayout('fresh')
				.setViews({
					'.header-top': new Header.Views.Top(),
					'.footer-end': new Footer.Views.End(),
					'.dates-upcoming': new Friends.Views.UpcomingDates(),
					'.friends-list-right': new Friends.Views.ListRight(),
					'.recent-activity': new Notifications.Views.RecentActivity(),
					'.top-leaderboard': new Leaderboard.Views.Top(),
					'.user-preview-medium': new UserPreview.Views.Medium(),
					'.user-preview-small': new UserPreview.Views.Small()
				}).render();
		},

		inbox: function () {
			app.useLayout('inbox')
				.setViews({
					'.header-top': new Header.Views.Top(),
					'.footer-end': new Footer.Views.End(),
					'.dates-upcoming': new Friends.Views.UpcomingDates(),
					'.friends-list-right': new Friends.Views.ListRight(),
					'.recent-activity': new Notifications.Views.RecentActivity(),
					'.top-leaderboard': new Leaderboard.Views.Top(),
					'.user-preview-medium': new UserPreview.Views.Medium(),
					'.user-preview-small': new UserPreview.Views.Small()
				}).render();
		},

		logout: function () {
			require(['Facebook'], function (Facebook) {
				Facebook.logout(function (response) {
				});
				Backbone.history.navigate('', true);
			});
		},

		matchmake: function () {
			app.useLayout('matchmake')
				.setViews({
					'.header-top': new Header.Views.Top(),
					'.footer-end': new Footer.Views.End(),
					'.dates-upcoming': new Friends.Views.UpcomingDates(),
					'.friends-list-right': new Friends.Views.ListRight(),
					'.recent-activity': new Notifications.Views.RecentActivity(),
					'.top-leaderboard': new Leaderboard.Views.Top(),
					'.user-preview-medium': new UserPreview.Views.Medium(),
					'.user-preview-small': new UserPreview.Views.Small()
				}).render();
		},

		leaderboard: function () {
			app.useLayout('leaderboard')
				.setViews({
					'.header-top': new Header.Views.Top(),
					'.footer-end': new Footer.Views.End(),
					'.dates-upcoming': new Friends.Views.UpcomingDates(),
					'.friends-list-right': new Friends.Views.ListRight(),
					'.recent-activity': new Notifications.Views.RecentActivity(),
					'.top-leaderboard': new Leaderboard.Views.Top(),
					'.user-preview-medium': new UserPreview.Views.Medium(),
					'.user-preview-small': new UserPreview.Views.Small()
				}).render();
		},

		message: function () {
			app.useLayout('message')
				.setViews({
					'.header-top': new Header.Views.Top(),
					'.footer-end': new Footer.Views.End(),
					'.dates-upcoming': new Friends.Views.UpcomingDates(),
					'.friends-list-right': new Friends.Views.ListRight(),
					'.recent-activity': new Notifications.Views.RecentActivity(),
					'.top-leaderboard': new Leaderboard.Views.Top(),
					'.user-preview-medium': new UserPreview.Views.Medium(),
					'.user-preview-small': new UserPreview.Views.Small()
				}).render();
		},

		profile: function () {
			app.useLayout('profile')
				.setViews({
					'.header-top': new Header.Views.Top(),
					'.footer-end': new Footer.Views.End(),
					'.dates-upcoming': new Friends.Views.UpcomingDates(),
					'.friends-list-right': new Friends.Views.ListRight(),
					'.recent-activity': new Notifications.Views.RecentActivity(),
					'.top-leaderboard': new Leaderboard.Views.Top(),
					'.user-preview-medium': new UserPreview.Views.Medium(),
					'.user-preview-small': new UserPreview.Views.Small()
				}).render();
		},
		
		terms: function (path) {
			app.useLayout('terms')
				.setViews({
					'.header-top': new Header.Views.Top(),
					'.footer-end': new Footer.Views.End(),
				}).render();
		}

	});
});
