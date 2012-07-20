define([
	'jQuery', 'Underscore', 'Backbone', 'app',
	'modules/Connections',
	'modules/Couple',
	'modules/Dates',
	'modules/Footer',
	'modules/Header',
	'modules/Message',
	'modules/Notifications',
	'modules/User'
], function (
	$, _, Backbone, app,
	Connections,
	Couple,
	Dates,
	Footer,
	Header,
	Message,
	Notifications,
	User
) {

	var viewGroups = {
			common: {
				'.bblm-header-top': Header.Views.Top,
				'.bblm-footer-end': Footer.Views.End
			},
			userPreviews: {
				'.bblm-user-preview-medium': User.Views.Medium,
				'.bblm-user-preview-points': User.Views.Points,
				'.bblm-user-preview-sexytime': User.Views.SexyTime,
				'.bblm-user-preview-small': User.Views.Small,
				'.bblm-user-preview-tiny': User.Views.Tiny
			},
			rightColumn: {
				'.bblm-dates-upcoming': Connections.Views.UpcomingDates,
				'.bblm-friends-list-right': Connections.Views.ListRight,
				'.bblm-recent-activity': Notifications.Views.RecentActivity,
				'.bblm-top-leaderboard': Connections.Views.LeaderboardTop,
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
					'.bblm-header-top': new Header.Views.Top({
						model: new User.Model(app.dummy.getMyProfile())
					}),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
		},

		about: function (path) {
			app.useLayout('about')
				.setViews({
					'.bblm-header-top': new Header.Views.Top({
						model: new User.Model(app.dummy.getMyProfile())
					}),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
		},

		dashboard: function () {
			var friends = new Connections.Collections.Friends(app.dummy.getFriends());
			var fbFriends = new Connections.Collections.FacebookFriends([], {id: app.user});
			app.useLayout('dashboard')
				.setViews({
					'.bblm-header-top': new Header.Views.Top({
						model: new User.Model(app.dummy.getMyProfile())
					}),
					'.bblm-footer-end': new Footer.Views.End(),
					'.bblm-dates-upcoming': new Connections.Views.UpcomingDates(),
					'.bblm-friends-list-right': new Connections.Views.ListRight({
						collection: friends
					}),
					'.bblm-recent-activity': new Notifications.Views.RecentActivity(),
					'.bblm-top-leaderboard': new Connections.Views.LeaderboardTop(),
					'.bblm-user-preview-medium': new User.Views.Medium(),
					'.bblm-user-preview-small': new User.Views.Small()
				}).render();
			fbFriends.fetch();
		},

		faq: function (path) {
			app.useLayout('faq')
				.setViews({
					'.bblm-header-top': new Header.Views.Top({
						model: new User.Model(app.dummy.getMyProfile())
					}),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
		},

		fresh: function () { /* TODO: merge into dashboard */
			var friends = new Connections.Collections.Friends(app.dummy.getFriends());
			app.useLayout('fresh')
				.setViews({
					'.bblm-header-top': new Header.Views.Top({
						model: new User.Model(app.dummy.getMyProfile())
					}),
					'.bblm-footer-end': new Footer.Views.End(),
					'.bblm-dates-upcoming': new Connections.Views.UpcomingDates(),
					'.bblm-friends-list-right': new Connections.Views.ListRight({
						collection: friends
					}),
					'.bblm-recent-activity': new Notifications.Views.RecentActivity(),
					'.bblm-top-leaderboard': new Connections.Views.LeaderboardTop(),
					'.bblm-user-preview-medium': new User.Views.Medium(),
					'.bblm-user-preview-small': new User.Views.Small()
				}).render();
		},

		inbox: function () {
			var friends = new Connections.Collections.Friends(app.dummy.getFriends());
			app.useLayout('inbox')
				.setViews({
					'.bblm-header-top': new Header.Views.Top({
						model: new User.Model(app.dummy.getMyProfile())
					}),
					'.bblm-footer-end': new Footer.Views.End(),
					'.bblm-dates-upcoming': new Connections.Views.UpcomingDates(),
					'.bblm-friends-list-right': new Connections.Views.ListRight({
						collection: friends
					}),
					'.bblm-message-summary': new Message.Views.Summary(),
					'.bblm-recent-activity': new Notifications.Views.RecentActivity(),
					'.bblm-top-leaderboard': new Connections.Views.LeaderboardTop(),
					'.bblm-user-preview-medium': new User.Views.Medium(),
					'.bblm-user-preview-small': new User.Views.Small()
				}).render();
		},

		landing: function () {
			app.useLayout('landing')
				.setViews({
					'.footer-end': new Footer.Views.End()
				}).render();
			require(['Facebook'], function (Facebook) {
				console.log('XFBML');
				Facebook.XFBML.parse();
			});
		},

		leaderboard: function () {
			draw('leaderboard', {
				'.bblm-leaderboard-full': new Connections.Views.LeaderboardFull({
					views: {
						'.bblm-user-preview-small': new User.Views.Small(), //sample how to load subviews… not very elegant.
						'.bblm-couple-preview': new Couple.Views.Preview()
					}
				})
			}, ['common', 'userPreviews', 'rightColumn']);
/*			app.useLayout('leaderboard')
				.setViews({
					'.bblm-leaderboard-full': new Connections.Views.LeaderboardFull(),
					'.bblm-header-top': new Header.Views.Top(),
					'.bblm-footer-end': new Footer.Views.End(),
					'.bblm-user-preview-medium': new User.Views.Medium(),
					'.bblm-user-preview-small': new User.Views.Small(),
					'.bblm-dates-upcoming': new Connections.Views.UpcomingDates(),
					'.bblm-friends-list-right': new Connections.Views.ListRight(),
					'.bblm-recent-activity': new Notifications.Views.RecentActivity(),
					'.bblm-top-leaderboard': new Connections.Views.LeaderboardTop(),

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
			var friends = new Connections.Collections.Friends(app.dummy.getFriends());
			app.useLayout('matchmake')
				.setViews({
					'.bblm-header-top': new Header.Views.Top({
						model: new User.Model(app.dummy.getMyProfile())
					}),
					'.bblm-footer-end': new Footer.Views.End(),
					'.bblm-dates-upcoming': new Connections.Views.UpcomingDates(),
					'.bblm-friends-list-right': new Connections.Views.ListRight({
						collection: friends
					}),
					'.bblm-recent-activity': new Notifications.Views.RecentActivity(),
					'.bblm-top-leaderboard': new Connections.Views.LeaderboardTop(),
					'.bblm-user-preview-medium': new User.Views.Medium(),
					'.bblm-user-preview-small': new User.Views.Small()
				}).render();
		},

		message: function () {
			var friends = new Connections.Collections.Friends(app.dummy.getFriends());
			app.useLayout('message')
				.setViews({
					'.bblm-header-top': new Header.Views.Top({
						model: new User.Model(app.dummy.getMyProfile())
					}),
					'.bblm-footer-end': new Footer.Views.End(),
					'.bblm-dates-upcoming': new Connections.Views.UpcomingDates(),
					'.bblm-friends-list-right': new Connections.Views.ListRight({
						collection: friends
					}),
					'.bblm-recent-activity': new Notifications.Views.RecentActivity(),
					'.bblm-top-leaderboard': new Connections.Views.LeaderboardTop(),
					'.bblm-user-preview-medium': new User.Views.Medium(),
					'.bblm-user-preview-small': new User.Views.Small()
				}).render();
		},

		profile: function (id) {
			var me = new User.Model(app.dummy.getMyProfile());
			// handle random profile
			var profile = new User.Model(app.dummy.getRandomProfile(id));
			if (id)
				profile = new User.Model(app.dummy.getProfile(id));
			var friends = new Connections.Collections.Friends(app.dummy.getFriends());

			var isMe = false;
			var isFriend = false;

			// testing dynamic routing
			var view = new User.Views.FofFullProfile({model: profile});
			if (me.id == profile.id) {
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
					'.bblm-header-top': new Header.Views.Top({model: me}),
					'.bblm-footer-end': new Footer.Views.End()
					
				}).render();
		},

		terms: function (path) {
			app.useLayout('terms')
				.setViews({
					'.bblm-header-top': new Header.Views.Top({
						model: me
					}),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
		},
		
		users: function () {
			var friends = new Connections.Collections.Friends(app.dummy.getFriends());
			app.useLayout('users')
				.setViews({
					'.bblm-header-top': new Header.Views.Top({
						model: new User.Model(app.dummy.getMyProfile())
					}),
					'.bblm-footer-end': new Footer.Views.End(),
					'.bblm-dates-upcoming': new Connections.Views.UpcomingDates(),
					'.bblm-friends-list-right': new Connections.Views.ListRight({
						collection: friends
					}),
					'.bblm-recent-activity': new Notifications.Views.RecentActivity(),
					'.bblm-top-leaderboard': new Connections.Views.LeaderboardTop(),
					'.bblm-user-preview-small': new User.Views.Small()
				}).render();
		}

	});
});
