define(['jQuery', 'Underscore', 'Mustache', 'Backbone', 'app'],
function($, _, Mustache, Backbone, app) {
	return {

		Model: Backbone.Model.extend({
		}),

		Collection: Backbone.Collection.extend({
		}),

		Views: {

			Medium: Backbone.View.extend({
				template: 'userpreview/medium'
			}),
			Small: Backbone.View.extend({
				template: 'userpreview/small'
			}),
			SexyTime: Backbone.View.extend({
				template: 'userpreview/sexytime'
			}),
			Points: Backbone.View.extend({
				template: 'userpreview/points'
			}),
			Tiny: Backbone.View.extend({
				template: 'userpreview/tiny'
			})

		}

	};
});
