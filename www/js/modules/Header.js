define(['jQuery', 'Underscore', 'Mustache', 'Backbone', 'app'],
function($, _, Mustache, Backbone, app) {
	return {

		Model: Backbone.Model.extend({
		}),

		Collection: Backbone.Collection.extend({
		}),

		Views: {

			Top: Backbone.View.extend({
				template: 'header'
			})
		}

	}

});