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
	Views.ListRight = Backbone.View.extend({
		template: 'friends/dates-upcoming',

		initialize: function () {
			this.collection.on('reset', this.render, this);
			
		},

		render: function (manage) {
			this.collection.each(function (user) {
				this.insertView('ul.bblm-user-preview-sexytime', new User.Views.SexyTime({
					model: user
				}));
			}, this);
			return manage(this).render();
		}
	});


	Views.ListRightCommon = Backbone.View.extend({
		template: 'friends/list-right-common'
	});

	Views.UpcomingDates = Backbone.View.extend({
		template: 'friends/dates-upcoming'
	});

	return {
		Model: Model,
		Collections: Collections,
		Views: Views
	};
});
