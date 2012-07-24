define(['jQuery', 'Underscore', 'Backbone', 'app'],
function($, _, Backbone, app) {

	var Collections = {},
		Views = {};

	var Model = Backbone.Model.extend({
	});

	Collections.Received = Backbone.Collection.extend({
		model: Model,
		url: function () {
			return app.api + 'activities/winks/';
		},
		parse: function (response) {
			return response.winks;
		}
	});

	Views.Received = Backbone.View.extend({
		template: 'winks/received',
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
