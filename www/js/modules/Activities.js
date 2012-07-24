define(['jQuery', 'Underscore', 'Backbone', 'app'],
function($, _, Backbone, app) {

	var Collections = {},
		Views = {};

	var Model = Backbone.Model.extend({
	});

	Collections.Recent = Backbone.Collection.extend({
		model: Model,
		url: function () {
			return app.api + 'activities/';
		},
		parse: function (response) {
			return response.activities;
		}
	});

	Views.Upcoming = Backbone.View.extend({
		template: 'activities/upcoming',
		initialize: function () {
			this.collection.on('reset', function () {
				this.render();
			}, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return {activities: this.collection.toJSON()};
		}
	});

	return {
		Model: Model,
		Collections: Collections,
		Views: Views
	};
});
