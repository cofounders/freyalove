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
			var deferred = manage(this).render();
			deferred.then(_.delay(_.bind(function () {
				slide.apply(this);
			}, this), 100));
			return deferred;
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
				begin = _.isFunction(this.begin) ? this.begin() : this.begin,
				floor = Math.max(0, Math.min(begin, lastAllowed));
			items.slice(floor, floor + this.step).forEach(selectItem);
			return {
				hasItems: items.length > 0,
				items: items,
				showNext: floor < items.length - 2,
				showPrevious: floor > 0
			};
		}
	}, Backbone.Events));
});
