define(['jQuery', 'Underscore', 'Backbone', 'app'],
function($, _, Backbone, app) {

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
				$(this.el).find('.name')
					.text(app.session.get('name'))
					.attr('href', '/profile/' + app.session.get('id'));
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
			'click .signout': function (event) {
				event.stopPropagation();
				event.preventDefault();
				app.session.signOut();
			},
			'click menu a': function (event) {
				event.stopPropagation();
				event.preventDefault();

			}
		}
	});

	Views.Public = Backbone.View.extend({
		template: 'header/public',
		events: {
			'click .button.facebook': function (event) {
				event.stopPropagation();
				event.preventDefault();
				app.session.signIn();
			}
		}
	});

	return {
		Model: Model,
		Collection: Collection,
		Views: Views
	};
});
