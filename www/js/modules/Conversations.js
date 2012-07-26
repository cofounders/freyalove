define(['jQuery', 'Underscore', 'Backbone', 'app'],
function($, _, Backbone, app) {
	var Collections = {},
		Views = {};

	var Model = Backbone.Model.extend({
	});

	Collections.Recent = Backbone.Collection.extend({
		model: Model,
		url: function () {
			return app.api + 'conversations/unread/';
		},
		parse: function (response) {
			return response.conversations;
		}
	});

	Views.Menu = Backbone.View.extend({
		template: 'conversations/menu',
		initialize: function () {
			this.collection.on('reset', function () {
				this.render();
			}, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return {conversations: this.collection.toJSON()};
		}
	});

	return {
		Model: Model,
		Collections: Collections,
		Views: Views
	};
});
