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
				/*
				var facebookPattern = new RegExp('^\\s*fb[^=]*' + app.fb_app_id),
					isFacebookCookie = function (cookie) { return facebookPattern.test(cookie); };
				document.cookie.split(';')
					.filter(isFacebookCookie)
					.forEach(function (cookie) {
						var name = cookie.substr(0, cookie.indexOf('=')),
							expires = (new Date(0)).toGMTString();
						console.log('name', name, 'expires', expires);
						document.cookie = name + '=; expires=' + expires
					});
				console.log('Reset cookies to', document.cookie);
				*/
				Backbone.history.navigate(app.root, true);
				event.stopPropagation();
				event.preventDefault();
			}
		}
	});

	Views.Public = Backbone.View.extend({
		template: 'header-public',
		events: {
			'click .button.facebook': function (event) {
				Facebook.login(function () {
					console.log('[Header] LOGGED IN');
					Backbone.history.navigate('/dashboard', true);
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
