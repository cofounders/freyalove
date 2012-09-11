define(['jQuery', 'Underscore', 'Backbone', 'app',
	'libs/url',
	'modules/Friends',
	'modules/Carousel',
	'modules/Dummy'
],
function($, _, Backbone, app,
	Url,
	Friends,
	Carousel,
	Dummy
) {

	var Models = {},
		Collections = {},
		Views = {};

	Models.Comparison = Backbone.Model.extend({
		initialize: function (options) {
			this.options = _.extend({
				users: []
			}, options);
		},
		url: function () {
			Url(app.api + '/matchmaker/:users/questions/answered/', {
				users: _.pluck(this.options.users, 'id')
			});
		},
		dummy: function () {
			this.set(Dummy.getComparison());
		}
	});

	Collections.Singles = Backbone.Collection.extend({
		model: Backbone.Model,
		url: function () {
			return Url(app.api + 'users/:id/matches/recommendations/', app.session);
		},
		dummy: function () {
			this.reset(Dummy.getMyPossibleMatches());
		}
	});

	Collections.Couples = Backbone.Collection.extend({
		model: Backbone.Model,
		url: function () {
			return app.api + 'matchmaker/recommendations/';
		},
		dummy: function () {
			this.reset(Dummy.getMatchingFriends());
		}
	});

	Views.Singles = Carousel.extend({
		template: 'matches/singles',
		begin: 1,
		step: 1,
		offset: function (index) {
			return -1 * (index - 1) * 230;
		}
	});

	Views.Couples = Carousel.extend({
		template: 'matches/couples',
		begin: 0,
		step: 2,
		width: 654 / 2
	});

	Views.Choice = Carousel.extend({
		template: 'matches/choice',
		begin: 1,
		step: 1,
		offset: function (index) {
			return -1 * (index - 1) * 230;
		}
	});

	Views.Comparison = Backbone.View.extend({
		template: 'matches/comparison',
		initialize: function (options) {
			this.options = _.extend({
				first: options.first || new Friends.Models.User(),
				second: options.second || new Friends.Models.User()
			}, options);
			this.model = new Models.Comparison(null, {
				users: [this.options.first, this.options.second]
			});
			this.model.on('change', this.render, this);
			this.options.first.model.on('change:id', this.model.fetch, this);
			this.options.second.model.on('change:id', this.model.fetch, this);
			this.options.first.on('slide', function (user) {
				this.options.first.model.set(user.attributes);
			});
			this.options.second.on('slide', function (user) {
				this.options.second.model.set(user.attributes);
			});
		},
		cleanup: function () {
			this.options.first.off(null, null, this);
			this.options.second.off(null, null, this);
		},
		serialize: function () {
			return this.model.toJSON();
		}
	});

	return {
		Models: Models,
		Collections: Collections,
		Views: Views
	};
});
