define([
	'jQuery',
	'Underscore',
	'Mustache',
	'Backbone',
	'GoogleAnalytics'
], function ($, _, Mustache, Backbone, GoogleAnalytics) {

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

		// The root path to run the application.
		root: '/',

		// Create a custom object with a nested Views object.
		module: function (additionalProps) {
			return _.extend({ Views: {} }, additionalProps);
		},

		// Helper for using layouts.
		useLayout: function (name) {
			// If already using this Layout, then don't re-inject into the DOM.
			if (this.layout && this.layout.options.template === name) {
				return this.layout;
			}

			// If a layout already exists, remove it from the DOM.
			if (this.layout) {
				this.layout.remove();
			}

			// Create a new Layout.
			var layout = new Backbone.Layout({
				template: name,
				className: "layout " + name,
				id: "layout"
			});

			// Insert into the DOM.
			$("#main").empty().append(layout.el);

			// Render the layout.
			layout.render();

			// Cache the refererence.
			this.layout = layout;

			// Return the reference, for chainability.
			return layout;
		}

	}, Backbone.Events);

});
