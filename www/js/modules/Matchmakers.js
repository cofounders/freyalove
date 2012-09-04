define(['jQuery', 'Underscore', 'Backbone', 'app', 'modules/Dummy'],
function($, _, Backbone, app, Dummy) {

	var Collections = {},
		Views = {};

	var Model = Backbone.Model.extend({
	});

	Collections.Top = Backbone.Collection.extend({
		model: Model,
		url: function () {
			return app.api + 'users/friends/leaderboard/summary/';
		},
		dummy: function () {
			this.reset(Dummy.getTopMatchmakers());
		}
	});

	Views.Top = Backbone.View.extend({
		template: 'matchmakers/top',
		initialize: function () {
			this.collection.on('reset', this.render, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return {matchmakers: this.collection.toJSON()};
		}
	});

	return {
		Model: Model,
		Collections: Collections,
		Views: Views
	};
});
