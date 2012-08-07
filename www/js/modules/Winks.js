define(['jQuery', 'Underscore', 'Backbone', 'app', 'modules/Carousel', 'modules/Dummy'],
function($, _, Backbone, app, Carousel, Dummy) {

	var Collections = {},
		Views = {};

	var Model = Backbone.Model.extend({
	});

	Collections.Received = Backbone.Collection.extend({
		model: Model,
		url: function () {
			return app.api + 'activities/winks/';
		},
		parse: function (response) {
			return response.winks;
		},
		dummy: function () {
			this.reset(Dummy.getWinks());
		}
	});

	Views.Received = Carousel.extend({
		template: 'winks/received',
		begin: 0,
		span: 4,
		width: 654 / 4
	});

	return {
		Model: Model,
		Collections: Collections,
		Views: Views
	};
});
