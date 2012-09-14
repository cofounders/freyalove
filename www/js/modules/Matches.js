define(['jQuery', 'Underscore', 'Backbone', 'app',
	'libs/url',
	'modules/Friends',
	'modules/Carousel',
	'modules/Dialog',
	'modules/Dummy'
],
function($, _, Backbone, app,
	Url,
	Friends,
	Carousel,
	Dialog,
	Dummy
) {

	var Models = {},
		Collections = {},
		Views = {};

	Models.Comparison = Backbone.Model.extend({
		initialize: function (attributes, options) {
			this.options = _.extend({
				users: []
			}, options);
		},
		url: function () {
			Url(app.api + 'matchmaker/:users/questions/answered/', {
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
		begin: function () {
			var selected = this.model.id;
				user = this.collection.find(function (user) {
					return user.id === selected;
				}),
				position = this.collection.indexOf(user);
			return Math.max(0, position);
		},
		step: 1,
		offset: function (index) {
			return -1 * (index - 1) * 130;
		}
	});

	Views.Comparison = Backbone.View.extend({
		template: 'matches/comparison',
		initialize: function (options) {
			var first = this.options.first,
				second = this.options.second,
				setUrl = function () {
					var url = Url('/matchmaker/:first/with/:second', {
							first: first.model.id,
							second: second.model.id
						});
					Backbone.history.navigate(url, {replace: true, silent: true});
				};
			this.model = new Models.Comparison(null, {
				users: [first, second]
			});
			this.model.on('change', function () {
				this.render();
			}, this);
			first.model.on('change:id', function () {
				this.model.fetch();
				setUrl();
			}, this);
			second.model.on('change:id', function () {
				this.model.fetch();
				setUrl();
			}, this);
			first.on('slide', function (user) {
				first.model.set(user.attributes);
			});
			second.on('slide', function (user) {
				second.model.set(user.attributes);
			});
		},
		cleanup: function () {
			this.options.first.off(null, null, this);
			this.options.second.off(null, null, this);
		},
		events: {
			'click .introduce .button.cta': function (event) {
				event.stopPropagation();
				event.preventDefault();
				var popup = new Views.Introduce({
					first: this.options.first.model,
					second: this.options.second.model
				});
				app.layout.insertViews({
					'.bblm-popup': popup
				});
				popup.render();
			}
		},
		serialize: function () {
			return {
				first: this.options.first.model.toJSON(),
				second: this.options.second.model.toJSON(),
				questions: this.model.toJSON()
			};
		}
	});

	Views.Introduce = Dialog.extend({
		template: 'matches/introduce',
		initialize: function (options) {
			this.options = options;
		},
		serialize: function () {
			return {
				first: this.options.first.toJSON(),
				second: this.options.second.toJSON()
			};
		},
		events: {
			'click .close': function (event) {
				event.stopPropagation();
				event.preventDefault();
				this.remove();
			},
			'click .button.primary': function (event) {
				event.stopPropagation();
				event.preventDefault();
				var popup = this;
				$.post(app.api + 'matchmaker/match/', {
					from: this.options.first.id,
					to: this.options.second.id
				}, function () {
					popup.remove();
				});
			}
		}
	});

	return {
		Models: Models,
		Collections: Collections,
		Views: Views
	};
});
