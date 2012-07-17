define([
	'jQuery',
	'Underscore',
	'Mustache',
	'Backbone',
	'plugins/backbone.layoutmanager',
	'Facebook'
], function ($, _, Mustache, Backbone, LayoutManager, Facebook) {

	var app = _.extend({
		el: $('#app'),
		root: '/',
		api: '/api/', // 'http://api.freyalove.cofounders.sg/api/',
		friends: [
			{firstName: "Sebastiaan"
			,lastName: "Deckers"
			,dateOfBirth: "09/05/1983"
			,about: "Lorem Ipsum Rockstar"
			,id: 1
			,profileImage: "/dummy/user2.png"},
			{firstName: "Wolf"
			,lastName: "Maehr"
			,dateOfBirth: "09/05/1973"
			,about: "UX Lorem Ipsum Rockstar"
			,id: 2
			,profileImage: "/dummy/user3.png"},
			{firstName: "Veron"
			,lastName: "Boobs"
			,dateOfBirth: "09/05/1988"
			,about: "Lorem Ipsum Tits"
			,id: 3
			,profileImage: "/dummy/user1.png"},
			{firstName: "Sayanee"
			,lastName: "Basu"
			,dateOfBirth: "09/08/1983"
			,about: "That's not even cleavage!"
			,id: 4
			,profileImage: "/dummy/user.png"},
		],
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
		}
	}, Backbone.Events);

	Backbone.LayoutManager.configure({
		paths: {
			layout: '/templates/layouts/',
			template: '/templates/views/'
		},
		fetch: function (path) { $.get(path + '.html', this.async()); },
		render: function (template, context) { return Mustache.to_html(template, context); }
	});

	return app;
});
