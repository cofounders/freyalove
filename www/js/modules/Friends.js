define(['jQuery', 'Underscore', 'Backbone', 'app', 'Facebook', 'modules/Dummy'],
function($, _, Backbone, app, Facebook, Dummy) {

	var Models = {},
		Collections = {},
		Views = {};

	Models.User = Backbone.Model.extend({
		url: function () {
			return app.api + 'users/' + this.id + '/profile/';
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
			return app.api + 'users/' + app.session.id + '/friends/';
		},
		parse: function (response) {
			return response.friends;
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
			return app.api + 'users/' + app.session.id + '/friends/'
				+ this.options.friend.id + '/mutual/';
		},
		parse: function (response) {
			return response.friends;
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
			var query = encodeURIComponent(this.options.query);
			return app.api + 'users/search/query/?q=' + query;
		},
		parse: function (response) {
			return response.friends;
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

	return {
		Models: Models,
		Collections: Collections,
		Views: Views
	};
});
