define(['jQuery', 'Underscore', 'Mustache', 'Backbone', 'app'],
function($, _, Mustache, Backbone, app) {
	return {

		Model: Backbone.Model.extend({
		}),

		Collection: Backbone.Collection.extend({
		}),

		Views: {

			Small: Backbone.View.extend({
				template: 'user-preview-small'
			}),
			Medium: Backbone.View.extend({
				template: 'user-preview-medium'
			}),
			Tiny: Backbone.View.extend({
				template: 'user-preview-tiny'
			})

		}

	};
});
