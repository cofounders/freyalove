define(['jQuery', 'Underscore', 'Mustache', 'Backbone', 'app'],
function($, _, Mustache, Backbone, app) {

	var Views = {};

	var Model = Backbone.Model.extend({
		initialize: function(models, options) {
		}
	});

	var Collection = Backbone.Collection.extend({
	});


	/*
	 * DEFINITION OF VIEWS
	 */
	

	// Show Header
	Views.Top = Backbone.View.extend({
		template: 'header',
		render: function (manage) {
			return manage(this).render(this.model.toJSON());
		}
	});


	return {
		Model: Model,
		Collection: Collection,
		Views: Views
	};
});