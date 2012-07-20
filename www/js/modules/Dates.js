define(['jQuery', 'Underscore', 'Mustache', 'Backbone', 'app', 'modules/User'],
function($, _, Mustache, Backbone, app, User) {

	var Collections = {},
		Views = {};

	var Model = Backbone.Model.extend({
		initialize: function(models, options) {
		}
	});

	Collections.UpcomingDates = Backbone.Collection.extend({

	});



	// VIEWS

	// Date list on the right hand friend panel
	Views.UpcomingDates = Backbone.View.extend({
		template: 'friends/dates-upcoming',
		serialize: function () {
			return _.extend({
				hasDates: (this.collection.length > 0)
			}, this.collection.toJSON());
		},
		render: function (manage) {
			this.collection.each(function (date) {
				this.insertView('ul.bblm-user-preview-sexytime', new User.Views.SexyTime({
					model: date
				}));
			}, this);
			return manage(this).render();
		}

	});

	return {
		Model: Model,
		Collections: Collections,
		Views: Views
	};
});
