define([
	'jQuery',
	'Underscore',
	'Mustache',
	'Backbone',
	'plugins/backbone.layoutmanager',
], function ($, _, Mustache, Backbone, LayoutManager) {

	var app = _.extend({
		el: $('#app'),
		root: '/',
		api: '/api/', // http://api.freyalove.cofounders.sg/',
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

	require(['Facebook'], function (Facebook) {
		Facebook.Event.subscribe('auth.authResponseChange', function (response) {
			console.log('[auth.authResponseChange] The status of the session is: ' + response.status);
			if (response.status === 'connected') {
				// Backbone.history.navigate('/dashboard', true);
			}
		});
		Facebook.Event.subscribe('auth.login', function (response) {
			console.log('[auth.login] The status of the session is: ' + response.status);
			// Backbone.history.navigate('/dashboard', true);
		});
		Facebook.init({
			appId      : '415866361791508', // App ID
			channelUrl : 'http://freyalove.cofounders.sg/channel.html', // Channel File
			status     : true, // check login status
			cookie     : true, // enable cookies to allow the server to access the session
			xfbml      : true  // parse XFBML
		});
		Facebook.XFBML.parse();
	});

	return app;
});
