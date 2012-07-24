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

		// Paths

		routes: {
			'': 'landing',
			'about': 'about',
			'dashboard': 'dashboard',
			'faq': 'faq',
 			'fresh': 'fresh', // TODO: merge into dashboard
			'inbox': 'inbox',
			'leaderboard': 'leaderboard',
			'matchmake': 'matchmake',
			'message': 'message',
			'profile/:id': 'profile', // TODO: merge fof and friends into this
			'profile/': 'profile', // placeholder for random user
			'profile': 'profile', // placeholder for random user
			'terms': 'terms',
			'users': 'users',
			'*path': '404'
		},

		// Handlers

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
			var fbFriends = new Connections.Collections.FacebookFriends([], {id: app.user}),
				winksReceived = new Winks.Collections.Received(),
				matchesSingles = new Matches.Collections.Singles(),
				matchesCouples = new Matches.Collections.Couples(),
				friendsAll = new Friends.Collections.All(),
				friendsCommon = new Friends.Collections.Common();
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
			fbFriends.fetch();
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

		fresh: function () { /* TODO: merge into dashboard */
			var friends = new Connections.Collections.Friends(app.dummy.getFriends());
			app.useLayout('fresh')
				.setViews({
					// left column
					'.bblm-user-preview-medium': new User.Views.Medium({
						collection: new Dates.Collections.UpcomingDates(app.dummy.getMyPossibleMatches())
					}),
					'.bblm-user-preview-small': new Connections.Views.ListWinks({
						collection: new Dates.Collections.UpcomingDates(app.dummy.getWinks())
					}),

					// right column
					'.bblm-dates-upcoming': new Connections.Views.UpcomingDates({
						collection: new Dates.Collections.UpcomingDates(app.dummy.getSexyTimes())
					}),
					'.bblm-friends-list-right': new Connections.Views.ListRight({
						collection: new Connections.Collections.Friends(app.dummy.getFriends())
					}),
					'.bblm-recent-activity': new Notifications.Views.RecentActivity(),
					'.bblm-top-leaderboard': new Connections.Views.LeaderboardTop(),

					// header & footer
					'.bblm-header-menu': new Header.Views.Menu(),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
		},

		inbox: function () {
			var friends = new Connections.Collections.Friends(app.dummy.getFriends());
			app.useLayout('inbox')
				.setViews({
					// left column

					// right column
					'.bblm-dates-upcoming': new Connections.Views.UpcomingDates({
						collection: new Dates.Collections.UpcomingDates(app.dummy.getSexyTimes())
					}),
					'.bblm-friends-list-right': new Connections.Views.ListRight({
						collection: new Connections.Collections.Friends(app.dummy.getFriends())
					}),
					'.bblm-recent-activity': new Notifications.Views.RecentActivity(),
					'.bblm-top-leaderboard': new Connections.Views.LeaderboardTop(),

					// header & footer
					'.bblm-header-menu': new Header.Views.Menu(
						),
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
					// left column
					'.bblm-leaderboard-full': new Connections.Views.LeaderboardFull(),

					// right column
					'.bblm-dates-upcoming': new Connections.Views.UpcomingDates({
						collection: new Dates.Collections.UpcomingDates(app.dummy.getSexyTimes())
					}),
					'.bblm-friends-list-right': new Connections.Views.ListRight({
						collection: new Connections.Collections.Friends(app.dummy.getFriends())
					}),
					'.bblm-recent-activity': new Notifications.Views.RecentActivity(),
					'.bblm-top-leaderboard': new Connections.Views.LeaderboardTop(),

					// header & footer
					'.bblm-header-menu': new Header.Views.Menu(),
					'.bblm-footer-end': new Footer.Views.End()

				});
		},

		matchmake: function () {
			var friends = new Connections.Collections.Friends(app.dummy.getFriends());
			app.useLayout('matchmake')
				.setViews({
					// main column


					// header & footer
					'.bblm-header-menu': new Header.Views.Menu(),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
		},

		message: function () {
			var friends = new Connections.Collections.Friends(app.dummy.getFriends());
			app.useLayout('message')
				.setViews({
					// left column

					// right column
					'.bblm-dates-upcoming': new Connections.Views.UpcomingDates({
						collection: new Dates.Collections.UpcomingDates(app.dummy.getSexyTimes())
					}),
					'.bblm-friends-list-right': new Connections.Views.ListRight({
						collection: new Connections.Collections.Friends(app.dummy.getFriends())
					}),
					'.bblm-recent-activity': new Notifications.Views.RecentActivity(),
					'.bblm-top-leaderboard': new Connections.Views.LeaderboardTop(),

					// header & footer
					'.bblm-header-menu': new Header.Views.Menu(),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
		},

		profile: function (id) {
			// handle random profile
			var profile = new User.Model(app.dummy.getRandomProfile(id));
			if (id)
				profile = new User.Model(app.dummy.getProfile(id));
			var friends = new Connections.Collections.Friends(app.dummy.getFriends());

			var isMe = false;
			var isFriend = false;

			// testing dynamic routing
			var view = new User.Views.FofFullProfile({model: profile});
			if (app.session.id === profile.id) {
				view = new User.Views.MyFullProfile({model: profile});
			} else if (friends.indexOf(profile) >= 0) {
				view = new User.Views.FriendFullProfile({model: profile, collection: friends});
				// TODO: remove collection once we have live data: friends, as that should be loaded in the module
			}
			app.useLayout('profile')
				.setViews({
					// left colum
					'.bblm-user-profile': view,

					// right column
					'.bblm-dates-upcoming': new Dates.Views.UpcomingDates({
						collection: new Dates.Collections.UpcomingDates(app.dummy.getSexyTimes())
					}),
					'.bblm-friends-list-right': new Connections.Views.ListRight({
						collection: friends
					}),
					'.bblm-recent-activity': new Notifications.Views.RecentActivity(),
					'.bblm-top-leaderboard': new Connections.Views.LeaderboardTop(),

					// header & footer
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
					// left column
					'.bblm-user-preview-small': new Connections.Views.ListWinks({
						collection: new Dates.Collections.UpcomingDates(app.dummy.getAllUsers())
					}),

					// right column
					'.bblm-dates-upcoming': new Connections.Views.UpcomingDates({
						collection: new Dates.Collections.UpcomingDates(app.dummy.getSexyTimes())
					}),
					'.bblm-friends-list-right': new Connections.Views.ListRight({
						collection: new Connections.Collections.Friends(app.dummy.getFriends())
					}),
					'.bblm-recent-activity': new Notifications.Views.RecentActivity(),
					'.bblm-top-leaderboard': new Connections.Views.LeaderboardTop(),

					// header & footer
					'.bblm-header-menu': new Header.Views.Menu(),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
		}

	});
});
