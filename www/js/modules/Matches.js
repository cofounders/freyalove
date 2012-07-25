define(['jQuery', 'Underscore', 'Mustache', 'Backbone', 'app'],
function($, _, Mustache, Backbone, app) {

	var Views = {},
		Collections = {};

	var Model = Backbone.Model.extend({
	});

	Collections.Singles = Backbone.Collection.extend({
		model: Model,
		url: function () {
			return app.api + 'users/' + app.session.id + '/matches/recommendations';
		},
		parse: function (response) {
			return response.matches;
		}
	});

	Collections.Couples = Backbone.Collection.extend({
		model: Model,
		url: function () {
			return app.api + 'matchmaker/recommendations';
		},
		parse: function (response) {
			return response.matches;
		}
	});

	Views.Singles = Backbone.View.extend({
		template: 'matches/singles',
		initialize: function () {
			this.collection.on('reset', function () {
				this.render();
			}, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return {matches: this.collection.toJSON()};
		}
	});


	Views.Couples = Backbone.View.extend({
		template: 'matches/couples',
		initialize: function () {
			this.collection.on('reset', function () {
				this.render();
			}, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return {matches: this.collection.toJSON()};
		}
	});

	return {
		Model: Model,
		Collections: Collections,
		Views: Views
	};
});