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
		template: 'header/menu',
		initialize: function (options) {
			app.session.on('change', this.render);
		},
		serialize: function () {
			return app.session.toJSON();
		},
		render: function (manage) {
			// new User.Model(app.dummy.getMyProfile())
			return manage(this).render();
		},
		events: {
			'click #nav-logout': function (event) {
				app.session.signOut();
				event.stopPropagation();
				event.preventDefault();
			}
		}
	});

	Views.Public = Backbone.View.extend({
		template: 'header/public',
		events: {
			'click .button.facebook': function (event) {
				app.session.signIn();
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
