define(['jQuery', 'Underscore', 'Backbone'],
function($, _, Backbone) {
	return Backbone.View.extend({
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
		slide: function () {
			var index = this.$('ol > .selected').index(),
				offsetLeft = -1 * (index - 1) * this.width,
				setDisabled = function (element, state) {
					element[state ? 'addClass' : 'removeClass']('disabled');
				};
			this.$('.viewport > ol').css('margin-left', offsetLeft + 'px');
			// this.$('.viewport > ol').css('transform', 'translateX(' + offsetLeft + 'px)');
			setDisabled(this.$('.previous'), index === 0);
			setDisabled(this.$('.next'), index === this.collection.length - 1);
		},
		serialize: function () {
			var items = this.collection.toJSON();
				selectItem = function (item) { item.selected = true; },
				forumula = function (a, b) { return b * (Math.ceil(a/b) - 1); },
				lastAllowed = forumula(items.length, this.span),
				begin = Math.max(0, Math.min(this.begin, lastAllowed));
			items.slice(begin, begin + this.span).forEach(selectItem);
			return {
				showPrevious: begin > 0,
				showNext: begin < items.length - 2,
				items: items
			};
		}
	});
});
