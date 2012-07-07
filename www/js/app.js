define([
	'jQuery',
	'Underscore',
	'Mustache',
	'Backbone',
	'plugins/backbone.layoutmanager'
], function ($, _, Mustache, Backbone, LayoutManager) {

	Backbone.LayoutManager.configure({

		paths: {
			layout: '/templates/layouts/',
			template: '/templates/views/'
		},

		fetch: function (path) {
			$.get(path + '.html', this.async());
		},

		render: function (template, context) {
			return Mustache.to_html(template, context);
		}

	});

	return _.extend({

		el: $('body'),

		root: '/',

		useLayout: function (name) {
			if (this.layout) {
				if (this.layout.options.template === name) {
					return this.layout;
				} else {
					this.layout.remove();
				}
			}

			this.layout = new Backbone.LayoutManager({
				className: 'layout ' + name,
				id: 'layout',
				template: name
			});

			this.el.empty().append(this.layout.el);
			this.layout.render();
			return this.layout;
		}

	}, Backbone.Events);

});
