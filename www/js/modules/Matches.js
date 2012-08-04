define(['jQuery', 'Underscore', 'Backbone', 'app', 'modules/Dummy'],
function($, _, Backbone, app, Dummy) {

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

	Views.Singles = Backbone.View.extend({
		template: 'matches/singles',
		initialize: function () {
			this.collection.on('reset', this.render, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		events: {
			'click .previous': function (event) {
				event.stopPropagation();
				event.preventDefault();
				if ($(event.target).is('.disabled')) return;
				this.$('ol > .selected').removeClass()
					.prev().addClass('selected')
					.filter(':first-child').addClass('disabled');
				this.slide();
			},
			'click .next': function (event) {
				event.stopPropagation();
				event.preventDefault();
				if ($(event.target).is('.disabled')) return;
				this.$('.selected').removeClass()
					.next().addClass('selected')
					.filter(':last-child').addClass('disabled');
				this.slide();
			}
		},
		width: 230,
		slide: function () {
			var index = this.$('ol > .selected').index();

			this.$('.viewport > ol').css('margin-left', (-1 * (index - 1) * this.width) + 'px');
			// this.$('.viewport > ol').css('transform', 'translateX(' + (-1 * (index - 1) * this.width) + 'px)');

			this.$('.previous')[index === 0 ? 'addClass' : 'removeClass']('disabled');
			this.$('.next')[(index === this.collection.length - 1) ? 'addClass' : 'removeClass']('disabled');
		},
		serialize: function () {
			var singles = this.collection.toJSON();
			if (singles.length === 1) singles[0].selected = true;
			else if (singles.length > 1) singles[1].selected = true;
			return {
				showPrevious: singles.length > 1,
				showNext: singles.length > 2,
				singles: singles
			};
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
