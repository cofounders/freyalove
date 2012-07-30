define(['jQuery', 'Underscore', 'Backbone', 'app'],
function($, _, Backbone, app) {
	return {

		Model: Backbone.Model.extend({
		}),

		Collection: Backbone.Collection.extend({
		}),

		Views: {

			Summary: Backbone.View.extend({
				template: 'message-summary'
			})

		}

	};
});
