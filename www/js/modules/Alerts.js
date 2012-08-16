define(['jQuery', 'Underscore', 'Backbone', 'app'],
function($, _, Backbone, app) {

	var Views = {};

	Views.Welcome = Backbone.View.extend({
		template: 'alerts/welcome',
		serialize: function () {
			var firstVisit = !app.session.has('firstVisit');
			if (firstVisit) {
				app.session.save('firstVisit', (new Date()).toISOString());
			}
			return {firstVisit: firstVisit};
		}
	});

	return {
		Views: Views
	};
});
