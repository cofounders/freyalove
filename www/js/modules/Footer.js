define(['jQuery', 'Underscore', 'Backbone', 'app'],
function($, _, Backbone, app) {
	return {

		Model: Backbone.Model.extend({
		}),

		Collection: Backbone.Collection.extend({
		}),

		Views: {

			End: Backbone.View.extend({
				template: 'footer'
			})

		}

	};
});
