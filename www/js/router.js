define([
	'jQuery', 'Underscore', 'Backbone', 'app', 'Facebook',
	'modules/Activities',
	'modules/Connections',
	'modules/Couple',
	'modules/Footer',
	'modules/Friends',
	'modules/Header',
	'modules/Matches',
	'modules/Matchmakers',
	'modules/Message',
	'modules/Notifications',
	'modules/SexyTimes',
	'modules/Sidebar',
	'modules/User',
	'modules/Winks'
], function (
	$, _, Backbone, app, Facebook,
	Activities,
	Connections,
	Couple,
	Footer,
	Friends,
	Header,
	Matches,
	Matchmakers,
	Message,
	Notifications,
	SexyTimes,
	Sidebar,
	User,
	Winks
) {
	return Backbone.Router.extend({

		routes: {
			'': 'landing',
			'about': 'about',
			'dashboard': 'dashboard',
			'faq': 'faq',
			'inbox': 'inbox',
			'leaderboard': 'leaderboard',
			'matchmake': 'matchmake',
			'message': 'message',
			'profile/:id': 'profile',
			'profile': 'profile',
			'terms': 'terms',
			'users': 'users',
			'*path': '404'
		},

		404: function (path) {
			app.useLayout('404')
				.setViews({
					'.bblm-header-public': new Header.Views.Public(),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
		},

		about: function (path) {
			app.useLayout('about')
				.setViews({
					'.bblm-header-public': new Header.Views.Public(),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
		},

		dashboard: function () {
			var winksReceived = new Winks.Collections.Received(),
				matchesSingles = new Matches.Collections.Singles(),
				matchesCouples = new Matches.Collections.Couples();
			app.useLayout('dashboard')
				.setViews({
					'.bblm-winks-received': new Winks.Views.Received({
						collection: winksReceived
					}),
					'.bblm-matches-singles': new Matches.Views.Singles({
						collection: matchesSingles
					}),
					'.bblm-matches-couples': new Matches.Views.Couples({
						collection: matchesCouples
					}),
					'.bblm-sidebar-panels': new Sidebar.Views.Panels(),
					'.bblm-header-menu': new Header.Views.Menu(),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
			winksReceived.fetch();
			matchesSingles.fetch();
			matchesCouples.fetch();
		},

		faq: function (path) {
			app.useLayout('faq')
				.setViews({
					'.bblm-header-public': new Header.Views.Public(),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
		},

		inbox: function () {
			var friends = new Connections.Collections.Friends(app.dummy.getFriends());
			app.useLayout('inbox')
				.setViews({
					'.bblm-sidebar-panels': new Sidebar.Views.Panels(),
					'.bblm-header-menu': new Header.Views.Menu(),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
		},

		landing: function () {
			app.useLayout('landing')
				.setViews({
					'.bblm-header-public': new Header.Views.Public(),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
		},

		leaderboard: function () {
			app.useLayout('leaderboard')
				.setViews({
					'.bblm-leaderboard-full': new Connections.Views.LeaderboardFull(),
					'.bblm-sidebar-panels': new Sidebar.Views.Panels(),
					'.bblm-header-menu': new Header.Views.Menu(),
					'.bblm-footer-end': new Footer.Views.End()
				});
		},

		matchmake: function () {
			var friends = new Connections.Collections.Friends(app.dummy.getFriends());
			app.useLayout('matchmake')
				.setViews({
					'.bblm-sidebar-panels': new Sidebar.Views.Panels(),
					'.bblm-header-menu': new Header.Views.Menu(),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
		},

		message: function () {
			var friends = new Connections.Collections.Friends(app.dummy.getFriends());
			app.useLayout('message')
				.setViews({
					'.bblm-sidebar-panels': new Sidebar.Views.Panels(),
					'.bblm-header-menu': new Header.Views.Menu(),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
		},

		profile: function (id) {
			var friends = new Backbone.Collection(),
				profile = id
					? new User.Model(app.dummy.getRandomProfile(id))
					: new User.Model(app.dummy.getProfile(id)),
				view = (app.session.id === profile.id) ? new User.Views.MyFullProfile({model: profile})
					: friends.contains(profile) ? new User.Views.FriendFullProfile({model: profile, collection: friends})
					: new User.Views.FofFullProfile({model: profile});
			app.useLayout('profile')
				.setViews({
					'.bblm-user-profile': view,
					'.bblm-sidebar-panels': new Sidebar.Views.Panels({
						friend: profile
					}),
					'.bblm-header-menu': new Header.Views.Menu(),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
		},

		terms: function (path) {
			app.useLayout('terms')
				.setViews({
					'.bblm-header-public': new Header.Views.Public(),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
		},

		users: function () {
			var friends = new Connections.Collections.Friends(app.dummy.getFriends());
			app.useLayout('users')
				.setViews({
					'.bblm-user-preview-small': new Connections.Views.ListWinks({
						collection: new Dates.Collections.UpcomingDates(app.dummy.getAllUsers())
					}),
					'.bblm-sidebar-panels': new Sidebar.Views.Panels(),
					'.bblm-header-menu': new Header.Views.Menu(),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
		}

	});
});
