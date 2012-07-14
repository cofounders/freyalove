define(['jQuery', 'Underscore', 'Mustache', 'Backbone', 'app', "modules/UserPreview"],
function($, _, Mustache, Backbone, app, UserPreview) {
	return {

		Model: Backbone.Model.extend({
			defaults: {name: "wolf", age: 65}
		}),

		Collection: Backbone.Collection.extend({
		}),

		Views: {

			ListRight: Backbone.View.extend({
				template: 'friends-list-right'
			}),

			UpcomingDates: Backbone.View.extend({
				template: 'dates-upcoming'
			})

		}

	};
});