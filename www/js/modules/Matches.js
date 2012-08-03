define(['jQuery', 'Underscore', 'Backbone', 'app'],
function($, _, Backbone, app) {

	var Collections = {},
		Views = {};

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
			this.collection.on('reset', this.render, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return {singles: this.collection.toJSON()};
		}
	});

	Views.Couples = Backbone.View.extend({
		template: 'matches/couples',
		initialize: function () {
			this.collection.on('reset', this.render, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return {couples: this.collection.toJSON()};
		}
	});

	Views.Matchmaker = Backbone.View.extend({
		template: 'matches/matchmaker',
		initialize: function () {
			this.collection.on('reset', this.render, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return {
				candidates: this.collection.toJSON(),
				first: this.options.first,
				second: this.options.second
			};
		}
	});

	return {
		Model: Model,
		Collections: Collections,
		Views: Views
	};
});
