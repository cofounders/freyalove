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
		},
		events: {
			'click #nav-logout': function (event) {
				app.session.signOut({success: function () {
					Backbone.history.navigate(app.root, true);
				}});
				event.stopPropagation();
				event.preventDefault();
			}
		}
	});

	Views.Public = Backbone.View.extend({
		template: 'header-public',
		events: {
			'click .button.facebook': function (event) {
				app.session.signIn({success: function () {
					Backbone.history.navigate('/dashboard', true);
				}});
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
