define(['jQuery', 'Underscore', 'Backbone', 'app'],
function($, _, Backbone, app) {

	var Collections = {},
		Views = {};

	var Model = Backbone.Model.extend({
	});

	Collections.Common = Backbone.Collection.extend({
		model: Model,
		initialize: function (models, options) {
			this.options = options || { friend: new Model() };
		},
		url: function () {
			return app.api + 'users/' + app.session.id + '/friends/'
				+ this.options.friend.id + '/mutual/';
		},
		parse: function (response) {
			return response.friends;
		}
	});

	Collections.All = Backbone.Collection.extend({
		model: Model,
		url: function () {
			return app.api + 'users/' + app.session.id + '/friends/';
		},
		parse: function (response) {
			return response.friends;
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
			return {winks: this.collection.toJSON()};
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
			return {winks: this.collection.toJSON()};
		}
	});

	return {
		Model: Model,
		Collections: Collections,
		Views: Views
	};
});
