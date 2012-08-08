define([
	'jQuery',
	'Underscore',
	'Handlebars',
	'Backbone',
	'plugins/backbone.layoutmanager',
	'constants',
	'modules/Dummy'
], function ($, _, Handlebars, Backbone, LayoutManager, constants, Dummy) {

	var app = _.extend({
		el: $('#app'),
		root: '/',
		api: '/api/', // http://api.freyalove.cofounders.sg/',
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
			// this.layout.render(); // Call render after setView(s)
			return this.layout;
		},
		constants: constants,
		dummy: Dummy
	}, Backbone.Events);

	var templateCache = _.memoize(Handlebars.compile);

	Backbone.LayoutManager.configure({
		paths: {
			layout: '/templates/layouts/',
			template: '/templates/views/'
		},
		fetch: function (path) { $.get(path + '.html', this.async()); },
		render: function (template, context) { return templateCache(template)(context); }
	});

	return app;
});
