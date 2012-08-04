define(['jQuery', 'Underscore', 'Backbone', 'app', 'modules/Carousel', 'modules/Dummy'],
function($, _, Backbone, app, Carousel, Dummy) {

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
		},
		fetch: function () {
			this.reset(Dummy.getMyPossibleMatches());
		}
	});

	Collections.Couples = Backbone.Collection.extend({
		model: Model,
		url: function () {
			return app.api + 'matchmaker/recommendations';
		},
		parse: function (response) {
			return response.matches;
		},
		fetch: function () {
			this.reset(Dummy.getMatchingFriends());
		}
	});

	Views.Singles = Carousel.extend({
		template: 'matches/singles',
		width: 230,
	}),

	Views.Couples = Carousel.extend({
		template: 'matches/couples',
		width: 230,
	}),

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
