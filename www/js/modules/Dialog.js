define(['jQuery', 'Underscore', 'Backbone'],
function($, _, Backbone) {
	return Backbone.View.extend(_.extend({
		initialize: function () {
			if (this.collection) {
				this.collection.on('reset', this.render, this);
			}
		},
		cleanup: function () {
			if (this.collection) {
				this.collection.off(null, null, this);
			}
		}
	}, Backbone.Events));
});
