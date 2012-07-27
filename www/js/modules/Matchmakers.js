define(['jQuery', 'Underscore', 'Backbone', 'app'],
function($, _, Backbone, app) {

	var Collections = {},
		Views = {};

	var Model = Backbone.Model.extend({
	});

	Collections.Top = Backbone.Collection.extend({
		model: Model,
		url: function () {
			return app.api + 'matchmakers/';
		},
		parse: function (response) {
			return response.matchmakers;
		}
	});

	Views.Top = Backbone.View.extend({
		template: 'matchmakers/top',
		initialize: function () {
			this.collection.on('reset', function () {
				this.render();
			}, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return {matchmakers: this.collection.toJSON()};
		},
		events: {
			'click .invite-more': function (event) {
				event.stopPropagation();
				event.preventDefault();
				Facebook.ui({
					method: 'apprequests',
					message: 'Matchmaking for lesbians',
					title: 'Join FreyaLove',
					filters: ['app_non_users']
				},
				function (response) {
				});
			}
		}
	});

	return {
		Model: Model,
		Collections: Collections,
		Views: Views
	};
});
