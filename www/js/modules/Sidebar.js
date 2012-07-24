define(['jQuery', 'Underscore', 'Mustache', 'Backbone', 'app'],
function($, _, Mustache, Backbone, app) {

	var Views = {};

	var Model = Backbone.Model.extend({
		initialize: function(models, options) {
		}
	});

	var Collection = Backbone.Collection.extend({
	});

	Views.Panels = Backbone.View.extend({
		template: 'sidebar/panels'
	});

	return {
		Model: Model,
		Collection: Collection,
		Views: Views
	};
});
