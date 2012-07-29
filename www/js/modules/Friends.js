define(['jQuery', 'Underscore', 'Backbone', 'app', 'Facebook', 'modules/Dummy'],
function($, _, Backbone, app, Facebook, Dummy) {

	var Collections = {},
		Views = {};

	var Model = Backbone.Model.extend({
	});

	Collections.All = Backbone.Collection.extend({
		model: Model,
		url: function () {
			return app.api + 'users/' + app.session.id + '/friends/';
		},
		parse: function (response) {
			return response.friends;
		},
		fetch: function () {
			this.reset(Dummy.getFriends());
		}
	});

	Collections.Common = Backbone.Collection.extend({
		model: Model,
		initialize: function (models, options) {
			this.options = options || {friend: new Model()};
		},
		url: function () {
			return app.api + 'users/' + app.session.id + '/friends/'
				+ this.options.friend.id + '/mutual/';
		},
		parse: function (response) {
			return response.friends;
		},
		fetch: function () {
			this.reset(Dummy.getMutualFriends());
		}
	});

	Collections.Search = Backbone.Collection.extend({
		model: Model,
		initialize: function (models, options) {
			this.options = options || {query: ''};
		},
		url: function () {
			return app.api + 'users/search/' + this.options.query;
		},
		parse: function (response) {
			return response.friends;
		},
		fetch: function () {
			this.reset(Dummy.getFriends());
		}
	});

	Views.All = Backbone.View.extend({
		template: 'friends/all',
		initialize: function () {
			this.collection.on('reset', function () {
				this.render();
			}, this);
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
			this.collection.on('reset', function () {
				this.render();
			}, this);
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
			this.collection.on('reset', function () {
				this.render();
			}, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return {
				count: this.collection.length,
				friends: this.collection.toJSON(),
				query: this.collection.options.query
			};
		}
	});

	return {
		Model: Model,
		Collections: Collections,
		Views: Views
	};
});
