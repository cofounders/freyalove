define(['jQuery', 'Underscore', 'Mustache', 'Backbone', 'app'],
function($, _, Mustache, Backbone, app) {
	return {

		Model: Backbone.Model.extend({
		}),

		Collection: Backbone.Collection.extend({
		}),

		Views: {

			Dates: Backbone.View.extend({
				template: 'user-preview-dates'
			}),
			Medium: Backbone.View.extend({
				template: 'user-preview-medium'
			}),
			Small: Backbone.View.extend({
				template: 'user-preview-small'
			}),
			Tiny: Backbone.View.extend({
				template: 'user-preview-tiny'
			})

		}

	};
});
