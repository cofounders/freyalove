define(['jQuery', 'Underscore', 'Mustache', 'Backbone', 'app', 'Facebook'],
function($, _, Mustache, Backbone, app, Facebook) {

	var Views = {};

	var Model = Backbone.Model.extend({
		initialize: function(models, options) {
		}
	});

	var Collection = Backbone.Collection.extend({
	});

	Views.Menu = Backbone.View.extend({
		template: 'header-menu',
		render: function (manage) {
			return manage(this).render(this.model.toJSON());
		}
	});

	Views.Public = Backbone.View.extend({
		template: 'header-public',
		events: {
			'click .button.facebook': function (event) {
				Facebook.login(function () {
					console.log('[Header] LOGGED IN');
				});
				event.stopPropagation();
				event.preventDefault();
			}
		}
	});

	return {
		Model: Model,
		Collection: Collection,
		Views: Views
	};
});