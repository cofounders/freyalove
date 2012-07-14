define(['jQuery', 'Underscore', 'Mustache', 'Backbone', 'app'],
function($, _, Mustache, Backbone, app) {
	return {

		Model: Backbone.Model.extend({
		}),

		Collection: Backbone.Collection.extend({
		}),

		Views: {

			Medium: Backbone.View.extend({
				template: 'user-preview-medium'
			}),
			Small: Backbone.View.extend({
				template: 'user-preview-small'
			}),
			SexyTime: Backbone.View.extend({
				template: 'user-preview-sexytime'
			}),
			Points: Backbone.View.extend({
				template: 'user-preview-points'
			}),
			Tiny: Backbone.View.extend({
				template: 'user-preview-tiny'
			})

		}

	};
});
