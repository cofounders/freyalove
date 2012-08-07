define([
	'jQuery', 'Underscore', 'Backbone', 'app',
	'modules/Conversations',
	'modules/Footer',
	'modules/Friends',
	'modules/Header',
	'modules/Matches',
	'modules/Sidebar',
	'modules/Winks'
], function (
	$, _, Backbone, app,
	Conversations,
	Footer,
	Friends,
	Header,
	Matches,
	Sidebar,
	Winks
) {
	return Backbone.Router.extend({

		routes: {
			'': 'landing',
			'about': 'about',
			'conversations/:id': 'conversation',
			'conversations/': 'conversations',
			'conversations': 'conversations',
			'dashboard': 'dashboard',
			'faq': 'faq',
			'matchmaker/:firstId/with/:secondId': 'matchmaker',
			'matchmaker/:firstId': 'matchmaker',
			'matchmaker': 'matchmaker',
			'profile/:id': 'profile',
			'profile/': 'profile',
			'profile': 'profile',
			'search/:query': 'search',
			'terms': 'terms',
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

		conversation: function (id) {
			var conversation = new Conversations.Models.Conversation({
					to: new Friends.Models.UserSummary({id: id})
				});
			app.useLayout('conversation')
				.setViews({
					'.bblm-conversations-conversation': new Conversations.Views.Conversation({
						model: conversation
					}),
					'.bblm-sidebar-panels': new Sidebar.Views.Panels(),
					'.bblm-header-menu': new Header.Views.Menu(),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
			conversation.fetch();
		},

		conversations: function () {
			var recentConversations = new Conversations.Collections.Recent();
			app.useLayout('conversations')
				.setViews({
					'.bblm-conversations-recent': new Conversations.Views.Recent({
						collection: recentConversations
					}),
					'.bblm-sidebar-panels': new Sidebar.Views.Panels(),
					'.bblm-header-menu': new Header.Views.Menu(),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
			recentConversations.fetch();
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

		landing: function () {
			app.useLayout('landing')
				.setViews({
					'.bblm-header-public': new Header.Views.Public(),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
		},

		matchmaker: function (firstId, secondId) {
			var candidates = new Friends.Collections.All();
			app.useLayout('matchmaker')
				.setViews({
					'.bblm-matches-matchmaker': new Matches.Views.Matchmaker({
						collection: candidates,
						first: new Friends.Models.User({id: firstId}),
						second: new Friends.Models.User({id: secondId})
					}),
					'.bblm-header-menu': new Header.Views.Menu(),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
			candidates.fetch();
		},

		profile: function (id) {
			var profile = new Friends.Models.User({id: id || app.session.id});
			// var friends = new Backbone.Collection(),
			// 	profile = id
			// 		? new User.Model(app.dummy.getRandomProfile(id))
			// 		: new User.Model(app.dummy.getProfile(id)),
			// 	view = (app.session.id === profile.id) ? new User.Views.MyFullProfile({model: profile})
			// 		: friends.contains(profile) ? new User.Views.FriendFullProfile({model: profile, collection: friends})
			// 		: new User.Views.FofFullProfile({model: profile});

			app.useLayout('profile')
				.setViews({
					'.bblm-user-profile': new Friends.Views.Profile({
						model: profile
					}),
					'.bblm-sidebar-panels': new Sidebar.Views.Panels({
						friend: profile
					}),
					'.bblm-header-menu': new Header.Views.Menu(),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
			profile.fetch();
		},

		search: function (query) {
			var searchResults = new Friends.Collections.Search(null, {
				query: decodeURIComponent(query)
			});
			app.useLayout('search')
				.setViews({
					'.bblm-friends-search': new Friends.Views.Search({
						collection: searchResults
					}),
					'.bblm-sidebar-panels': new Sidebar.Views.Panels(),
					'.bblm-header-menu': new Header.Views.Menu(),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
			searchResults.fetch();
		},

		terms: function (path) {
			app.useLayout('terms')
				.setViews({
					'.bblm-header-public': new Header.Views.Public(),
					'.bblm-footer-end': new Footer.Views.End()
				}).render();
		}

	});
});
