define(['jQuery', 'Underscore', 'Backbone', 'app'],
function($, _, Backbone, app) {

	var Collections = {},
		Views = {};

	var Model = Backbone.Model.extend({
	});

	Collections.Top = Backbone.Collection.extend({
		model: Model,
		url: function () {
			return app.api + 'matchmakers/';
		},
		parse: function (response) {
			return response.matchmakers;
		}
	});

	Views.Upcoming = Backbone.View.extend({
		template: 'matchmakers/top',
		initialize: function () {
			this.collection.on('reset', function () {
				this.render();
			}, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return {matchmakers: this.collection.toJSON()};
		}
	});

	return {
		Model: Model,
		Collections: Collections,
		Views: Views
	};
});
