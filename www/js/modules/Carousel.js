define(['jQuery', 'Underscore', 'Backbone'],
function($, _, Backbone) {
	var slide = function () {
			var index = this.$('ol > .selected').first().index(),
				offsetLeft = this.offset(index),
				setDisabled = function (element, state) {
					element[state ? 'addClass' : 'removeClass']('disabled');
				};
			this.$('.viewport > ol').css('margin-left', offsetLeft + 'px');
			// this.$('.viewport > ol').css('transform', 'translateX(' + offsetLeft + 'px)');
			setDisabled(this.$('.previous'), index === 0);
			setDisabled(this.$('.next'), index === this.collection.length - 1);
			this.trigger('slide', this.collection.at(index));
		};
	return Backbone.View.extend(_.extend({
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
				this.$('.selected').removeClass()
					.first().prevAll().slice(0, this.step).addClass('selected')
					.filter(':first-child').addClass('disabled');
				slide.apply(this);
			},
			'click .next': function (event) {
				event.stopPropagation();
				event.preventDefault();
				if ($(event.target).is('.disabled')) return;
				this.$('.selected').removeClass()
					.last().nextAll().slice(0, this.step).addClass('selected')
					.filter(':last-child').addClass('disabled');
				slide.apply(this);
			}
		},
		render: function (manage) {
			var begin = Math.min(this.begin, this.collection.length - 1);
			this.trigger('slide', this.collection.at(begin));
			return manage(this).render();
		},
		offset: function (index) {
			return -1 * index * this.width;
		},
		begin: 0,
		step: 1,
		width: 200,
		collection: new Backbone.Collection,
		serialize: function () {
			var items = this.collection.toJSON(),
				selectItem = function (item) { item.selected = true; },
				formula = function (a, b) { return b * (Math.ceil(a/b) - 1); },
				lastAllowed = formula(items.length, this.step),
				begin = Math.max(0, Math.min(this.begin, lastAllowed));
			items.slice(begin, begin + this.step).forEach(selectItem);
			return {
				hasItems: items.length > 0,
				items: items,
				showNext: begin < items.length - 2,
				showPrevious: begin > 0
			};
		}
	}, Backbone.Events));
});
