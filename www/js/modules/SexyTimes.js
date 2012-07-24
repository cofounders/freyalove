define(['jQuery', 'Underscore', 'Backbone', 'app'],
function($, _, Backbone, app) {

	var Collections = {},
		Views = {};

	var Model = Backbone.Model.extend({
	});

	Collections.Upcoming = Backbone.Collection.extend({
		model: Model,
		url: function () {
			return app.api + 'users/sexytimes/';
		},
		parse: function (response) {
			return response.sexytimes;
		}
	});

	Views.Upcoming = Backbone.View.extend({
		template: 'sexytimes/upcoming',
		initialize: function () {
			this.collection.on('reset', function () {
				this.render();
			}, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return _.extend({
				hasDates: (this.collection.length > 0)
			}, this.collection.toJSON());
		},
		// render: function (manage) {
		// 	this.collection.each(function (date) {
		// 		this.insertView('ul.bblm-user-preview-sexytime', new User.Views.SexyTime({
		// 			model: date
		// 		}));
		// 	}, this);
		// 	return manage(this).render();
		// }
	});

	return {
		Model: Model,
		Collections: Collections,
		Views: Views
	};
});
