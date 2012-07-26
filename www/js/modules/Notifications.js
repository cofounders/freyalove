define(['jQuery', 'Underscore', 'Backbone', 'app'],
function($, _, Backbone, app) {
	var Collections = {},
		Views = {};

	var Model = Backbone.Model.extend({
	});

	Collections.Recent = Backbone.Collection.extend({
		model: Model,
		url: function () {
			return app.api + 'notifications/unread/';
		},
		parse: function (response) {
			return response.notifications;
		}
	});

	Views.RecentActivity = Backbone.View.extend({
		template: 'recent-activity'
	});

	Views.Menu = Backbone.View.extend({
		template: 'notifications/menu',
		initialize: function () {
			this.collection.on('reset', function () {
				this.render();
			}, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return {notifications: this.collection.toJSON()};
		}
	});

	return {
		Model: Model,
		Collections: Collections,
		Views: Views
	};
});
