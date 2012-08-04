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
			var index = this.$('ol > .selected').index();

			this.$('.viewport > ol').css('margin-left', (-1 * (index - 1) * this.width) + 'px');
			// this.$('.viewport > ol').css('transform', 'translateX(' + (-1 * (index - 1) * this.width) + 'px)');

			this.$('.previous')[index === 0 ? 'addClass' : 'removeClass']('disabled');
			this.$('.next')[(index === this.collection.length - 1) ? 'addClass' : 'removeClass']('disabled');
		},
		serialize: function () {
			var items = this.collection.toJSON();
			if (items.length === 1) items[0].selected = true;
			else if (items.length > 1) items[1].selected = true;
			return {
				showPrevious: items.length > 1,
				showNext: items.length > 2,
				items: items
			};
		}
	});
});
