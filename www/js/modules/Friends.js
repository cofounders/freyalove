define(['jQuery', 'Underscore', 'Backbone', 'app',
	'Facebook',
	'libs/url',
	'modules/ProfileTabs',
	'modules/Dummy'
],
function($, _, Backbone, app,
	Facebook,
	Url,
	ProfileTabs,
	Dummy
) {

	var Models = {},
		Collections = {},
		Views = {};

	Models.User = Backbone.Model.extend({
		url: function () {
			return Url(app.api + 'users/:id/profile/', this);
		},
		dummy: function () {
			this.clear({silent: true});
			this.set(this.id === app.session.id
				? Dummy.getMyProfile()
				: Dummy.getRandomProfile()
			);
		}
	});

	Models.UserSummary = Backbone.Model.extend({
	});

	Collections.All = Backbone.Collection.extend({
		model: Models.UserSummary,
		url: function () {
			return Url(app.api + 'users/:id/friends/', app.session);
		},
		dummy: function () {
			this.reset(Dummy.getFriends());
		}
	});

	Collections.Common = Backbone.Collection.extend({
		model: Models.UserSummary,
		initialize: function (models, options) {
			this.options = options || {friend: new Models.UserSummary()};
		},
		url: function () {
			return Url(app.api + 'users/:me/friends/:friend/mutual/', {
				me: app.session.id,
				friend: this.options.friend.id
			});
		},
		dummy: function () {
			this.reset(Dummy.getMutualFriends());
		}
	});

	Collections.Search = Backbone.Collection.extend({
		model: Models.UserSummary,
		initialize: function (models, options) {
			this.options = options || {query: ''};
		},
		url: function () {
			return Url(app.api + 'users/search/query/?q=:query', this.options);
		},
		dummy: function () {
			this.reset(Dummy.getFriends());
		}
	});

	Views.All = Backbone.View.extend({
		template: 'friends/all',
		initialize: function () {
			this.collection.on('reset', this.render, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return {
				count: this.collection.length,
				friends: this.collection.toJSON()
			};
		},
		events: {
			'click .invite-more': function (event) {
				event.stopPropagation();
				event.preventDefault();
				Facebook.ui({
					method: 'apprequests',
					message: 'Matchmaking for lesbians',
					title: 'Join FreyaLove',
					filters: ['app_non_users']
				},
				function (response) {
				});
			}
		}
	});

	Views.Common = Backbone.View.extend({
		template: 'friends/common',
		initialize: function () {
			this.collection.on('reset', this.render, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return {
				count: this.collection.length,
				friends: this.collection.toJSON()
			};
		}
	});

	Views.Search = Backbone.View.extend({
		template: 'friends/search',
		initialize: function () {
			this.collection.on('reset', this.render, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			var friends = _.map(this.collection.toJSON(), function (friend) {
					var dob = new Date(friend.dateOfBirth),
						months = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split(' ');
					friend.prettyDateOfBirth = (/^\d{4}/.test(friend.dateOfBirth))
						? months[dob.getMonth()] + ' ' + dob.getDate() + ', ' + dob.getFullYear()
						: dob.getDate() + ', ' + dob.getFullYear();
					return friend;
				});
			return {
				count: this.collection.length,
				friends: friends,
				query: this.collection.options.query
			};
		}
	});

	Views.Profile = Backbone.View.extend({
		template: 'friends/profile',
		initialize: function () {
			this.model.on('change', function () {
				this.render();
			}, this);
		},
		cleanup: function () {
			this.model.off(null, null, this);
		},
		serialize: function () {
			return {
				friend: _.extend({
					isMe: app.session.id === this.model.id,
					isFriend: !!this.model.get('isFriend'),
					isFof: !this.model.get('isFriend')
						&& app.session.id !== this.model.id
				}, this.model.toJSON())
			};
		}
	});

	Views.Tabs = Backbone.View.extend({
		template: 'friends/tabs',
		initialize: function (options) {
			this.options = _.extend(options || {}, {
				tabs: ProfileTabs.Tabs
			});
		},
		render: function (manage) {
			var deferred = manage(this).render(),
				view = this,
				drawTab = _.bind(function (tab, menu) {
					var button = $('<li></li>')
						.text(tab.name)
						.click(function (event) {
							event.stopPropagation();
							var panel = view.$('article').html(''),
								content = new tab.view();
							view.$('menu > li.active').removeClass('active');
							$(this).addClass('active');
							view
								.insertView('article', content)
								.render();
						});
					menu.append(button);
					if (tab.tabs) {
						var submenu = $('<menu></menu>');
						button.append(submenu);
						_.each(tab.tabs, function (tab) {
							drawTab(tab, submenu);
						});
					}
				}, this);
			deferred.then(_.bind(function () {
				var menu = this.$('menu');
				_.each(this.options.tabs, function (tab) {
					drawTab(tab, menu);
				});
				this.$('menu > li').first().click();
			}, this));
			return deferred;
		}
	});

	return {
		Models: Models,
		Collections: Collections,
		Views: Views
	};
});
