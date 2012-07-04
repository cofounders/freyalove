define([
	'jQuery',
	'Underscore',
	'Mustache',
	'Backbone',
	'plugins/backbone.layoutmanager',
	'GoogleAnalytics'
], function ($, _, Mustache, Backbone, LayoutManager, GoogleAnalytics) {

	GoogleAnalytics.track('UA-32964267-1');

	// Configure LayoutManager with Backbone Boilerplate defaults.
	Backbone.LayoutManager.configure({

		paths: {
			layout: 'templates/layouts/',
			template: 'templates/'
		},

		fetch: function (path) {
			$.get(name, this.async());
		},

		render: function (template, context) {
			return Mustache.to_html(template, context);
		}

	});

	return _.extend({

		root: '/',

		// Create a custom object with a nested Views object.
		module: function (additionalProps) {
			return _.extend({ Views: {} }, additionalProps);
		},

		useLayout: function (name) {
			if (this.layout) {
				if (this.layout.options.template === name) {
					return this.layout;
				} else {
					this.layout.remove();
				}
			}

			this.layout = new Backbone.Layout({
				template: name,
				className: "layout " + name,
				id: "layout"
			});

			$("#main").empty().append(this.layout.el);
			this.layout.render();
			return this.layout;
		}

	}, Backbone.Events);

});
