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
			app.session.on('change:name', function () {
				$(this.el).find('#nav-name').text(app.session.get('name'));
			}, this);
		},
		cleanup: function () {
			app.session.off(null, null, this);
		},
		serialize: function () {
			return app.session.toJSON();
		},
		render: function (manage) {
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
