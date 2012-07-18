define([
	'jQuery', 'Underscore', 'Backbone', 'app',
	'modules/Couple',
	'modules/Dates',
	'modules/Dummy', // TODO: remove dummy eventually
	'modules/Footer',
	'modules/Friends',
	'modules/Header',
	'modules/Message',
	'modules/Notifications',
	'modules/UserPreview'
], function (
	$, _, Backbone, app,
	Couple,
	Dates,
	Dummy, // TODO: remove dummy eventually
	Footer,
	Friends,
	Header,
	Message,
	Notifications,
	UserPreview
) {

	var viewGroups = {
			common: {
				'.bblm-header-top': Header.Views.Top,
				'.bblm-footer-end': Footer.Views.End
			},
			userPreviews: {
				'.bblm-user-preview-medium': UserPreview.Views.Medium,
				'.bblm-user-preview-points': UserPreview.Views.Points,
				'.bblm-user-preview-sexytime': UserPreview.Views.SexyTime,
				'.bblm-user-preview-small': UserPreview.Views.Small,
				'.bblm-user-preview-tiny': UserPreview.Views.Tiny
			},
			rightColumn: {
				'.bblm-dates-upcoming': Friends.Views.UpcomingDates,
				'.bblm-friends-list-right': Friends.Views.ListRight,
				'.bblm-recent-activity': Notifications.Views.RecentActivity,
				'.bblm-top-leaderboard': Friends.Views.LeaderboardTop,
			}
		},
		draw = function (layout, views, presets) {
			var selectedPresets = _.map(presets, function (preset) {
					var instantiatedPresets = {};
					_.each(viewGroups[preset], function (signature, selector) {
						instantiatedPresets[selector] = new signature();
					});
					return instantiatedPresets;
				}),
				selectedViews = _.extend.apply(null, [{}, views].concat(selectedPresets));
			app.useLayout(layout).setViews(selectedViews).render();
		};

	return Backbone.Router.extend({

		// Paths

		routes: {
			'': 'landing',
			'about': 'about',
			'dashboard': 'dashboard',
			'faq': 'faq',
 			'fresh': 'fresh', // TODO: merge into dashboard
			'inbox': 'inbox',
			'leaderboard': 'leaderboard',
			'logout': 'logout',
			'matchmake': 'matchmake',
			'message': 'message',
			'profile/:id': 'profile', // TODO: merge fof and friends into this
			'terms': 'terms',
			'users': 'users',
			'*path': '404'
		},

		// Handlers

		404: function (path) {
			app.useLayout('404')
				.setViews({
					'.bblm-header-top': new Header.Views.Top(),
					'.bblm-footer-end': new Footer.Views.End(),
				}).render();
		},

		about: function (path) {
			app.useLayout('about')
				.setViews({
					'.bblm-header-top': new Header.Views.Top(),
					'.bblm-footer-end': new Footer.Views.End(),
				}).render();
		},

		dashboard: function () {
			var friends = new Friends.Collection(Dummy.getFriends());
			app.useLayout('dashboard')
				.setViews({
					'.bblm-header-top': new Header.Views.Top(),
					'.bblm-footer-end': new Footer.Views.End(),
					'.bblm-dates-upcoming': new Friends.Views.UpcomingDates(),
					'.bblm-friends-list-right': new Friends.Views.ListRight({
						collection: friends
					}),
					'.bblm-recent-activity': new Notifications.Views.RecentActivity(),
					'.bblm-top-leaderboard': new Friends.Views.LeaderboardTop(),
					'.bblm-user-preview-medium': new UserPreview.Views.Medium(),
					'.bblm-user-preview-small': new UserPreview.Views.Small()
				}).render();
//			friends.fetch();
		},
		
		faq: function (path) {
			app.useLayout('faq')
				.setViews({
					'.bblm-header-top': new Header.Views.Top(),
					'.bblm-footer-end': new Footer.Views.End(),
				}).render();
		},

		fresh: function () { /* TODO: merge into dashboard */
			app.useLayout('fresh')
				.setViews({
					'.bblm-header-top': new Header.Views.Top(),
					'.bblm-footer-end': new Footer.Views.End(),
					'.bblm-dates-upcoming': new Friends.Views.UpcomingDates(),
					'.bblm-friends-list-right': new Friends.Views.ListRight(),
					'.bblm-recent-activity': new Notifications.Views.RecentActivity(),
					'.bblm-top-leaderboard': new Friends.Views.LeaderboardTop(),
					'.bblm-user-preview-medium': new UserPreview.Views.Medium(),
					'.bblm-user-preview-small': new UserPreview.Views.Small()
				}).render();
		},

		inbox: function () {
			app.useLayout('inbox')
				.setViews({
					'.bblm-header-top': new Header.Views.Top(),
					'.bblm-footer-end': new Footer.Views.End(),
					'.bblm-dates-upcoming': new Friends.Views.UpcomingDates(),
					'.bblm-friends-list-right': new Friends.Views.ListRight(),
					'.bblm-message-summary': new Message.Views.Summary(),
					'.bblm-recent-activity': new Notifications.Views.RecentActivity(),
					'.bblm-top-leaderboard': new Friends.Views.LeaderboardTop(),
					'.bblm-user-preview-medium': new UserPreview.Views.Medium(),
					'.bblm-user-preview-small': new UserPreview.Views.Small()
				}).render();
		},

		landing: function () {
			app.useLayout('landing')
				.setViews({
					'.footer-end': new Footer.Views.End()
				}).render();
		},

		leaderboard: function () {
			draw('leaderboard', {
				'.bblm-leaderboard-full': new Friends.Views.LeaderboardFull({
					views: {
						'.bblm-user-preview-small': new UserPreview.Views.Small(), //sample how to load subviews… not very elegant.
						'.bblm-couple-preview': new Couple.Views.Preview()
					}
				})
			}, ['common', 'userPreviews', 'rightColumn']);
/*			app.useLayout('leaderboard')
				.setViews({
					'.bblm-leaderboard-full': new Friends.Views.LeaderboardFull(),
					'.bblm-header-top': new Header.Views.Top(),
					'.bblm-footer-end': new Footer.Views.End(),
					'.bblm-user-preview-medium': new UserPreview.Views.Medium(),
					'.bblm-user-preview-small': new UserPreview.Views.Small(),
					'.bblm-dates-upcoming': new Friends.Views.UpcomingDates(),
					'.bblm-friends-list-right': new Friends.Views.ListRight(),
					'.bblm-recent-activity': new Notifications.Views.RecentActivity(),
					'.bblm-top-leaderboard': new Friends.Views.LeaderboardTop(),

				});*/
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
					'.bblm-header-top': new Header.Views.Top(),
					'.bblm-footer-end': new Footer.Views.End(),
					'.bblm-dates-upcoming': new Friends.Views.UpcomingDates(),
					'.bblm-friends-list-right': new Friends.Views.ListRight(),
					'.bblm-recent-activity': new Notifications.Views.RecentActivity(),
					'.bblm-top-leaderboard': new Friends.Views.LeaderboardTop(),
					'.bblm-user-preview-medium': new UserPreview.Views.Medium(),
					'.bblm-user-preview-small': new UserPreview.Views.Small()
				}).render();
		},

		message: function () {
			app.useLayout('message')
				.setViews({
					'.bblm-header-top': new Header.Views.Top(),
					'.bblm-footer-end': new Footer.Views.End(),
					'.bblm-dates-upcoming': new Friends.Views.UpcomingDates(),
					'.bblm-friends-list-right': new Friends.Views.ListRight(),
					'.bblm-recent-activity': new Notifications.Views.RecentActivity(),
					'.bblm-top-leaderboard': new Friends.Views.LeaderboardTop(),
					'.bblm-user-preview-medium': new UserPreview.Views.Medium(),
					'.bblm-user-preview-small': new UserPreview.Views.Small()
				}).render();
		},

		profile: function (id) {
			var profile = new UserPreview.Model({id: id});
			app.useLayout('profile')
				.setViews({
					'.bblm-header-top': new Header.Views.Top(),
					'.bblm-footer-end': new Footer.Views.End(),
					'.bblm-user-profile': new User.Views.FullProfile({
						model: profile
					}),
					'.bblm-dates-upcoming': new Friends.Views.UpcomingDates(),
					'.bblm-friends-list-right': new Friends.Views.ListRight(),
					'.bblm-recent-activity': new Notifications.Views.RecentActivity(),
					'.bblm-top-leaderboard': new Friends.Views.LeaderboardTop(),
					'.bblm-user-preview-medium': new UserPreview.Views.Medium(),
					'.bblm-user-preview-small': new UserPreview.Views.Small()
				}).render();
		},
		
		terms: function (path) {
			app.useLayout('terms')
				.setViews({
					'.bblm-header-top': new Header.Views.Top(),
					'.bblm-footer-end': new Footer.Views.End(),
				}).render();
		},
		
		users: function () {
			app.useLayout('users')
				.setViews({
					'.bblm-header-top': new Header.Views.Top(),
					'.bblm-footer-end': new Footer.Views.End(),
					'.bblm-dates-upcoming': new Friends.Views.UpcomingDates(),
					'.bblm-friends-list-right': new Friends.Views.ListRight(),
					'.bblm-recent-activity': new Notifications.Views.RecentActivity(),
					'.bblm-top-leaderboard': new Friends.Views.LeaderboardTop(),
					'.bblm-user-preview-small': new UserPreview.Views.Small()
				}).render();
		}

	});
});
