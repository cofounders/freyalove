define(['jQuery', 'Underscore', 'Backbone', 'app', 'modules/Dummy'],
function($, _, Backbone, app, Dummy) {

	var Collections = {},
		Views = {};

	var Model = Backbone.Model.extend({
	});

	Collections.Upcoming = Backbone.Collection.extend({
		model: Model,
		url: function () {
			return app.api + 'activities/sexytimes/';
		},
		parse: function (response) {
			return response.sexytimes;
		},
		fetch: function () {
			this.reset(Dummy.getSexyTimes());
		}
	});

	Views.Upcoming = Backbone.View.extend({
		template: 'sexytimes/upcoming',
		initialize: function () {
			this.collection.on('reset', this.render, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return {sexyTimes: this.collection.toJSON()};
		}
	});

	Views.Menu = Backbone.View.extend({
		template: 'sexytimes/menu',
		initialize: function () {
			this.collection.on('reset', this.render, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return {sexyTimes: this.collection.toJSON()};
		}
	});

	return {
		Model: Model,
		Collections: Collections,
		Views: Views
	};
});
