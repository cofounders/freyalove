require.config({

	baseUrl: '/js',

	deps: ['main'],

	paths: {
		Backbone: '//cdnjs.cloudflare.com/ajax/libs/backbone.js/0.9.2/backbone-min',
		Facebook: '//connect.facebook.net/en_US/all',
		Handlebars: '//cdnjs.cloudflare.com/ajax/libs/handlebars.js/1.0.0.beta6/handlebars.min',
		jQuery: '//cdnjs.cloudflare.com/ajax/libs/jquery/1.7.2/jquery.min',
		Underscore: '//cdnjs.cloudflare.com/ajax/libs/lodash.js/0.3.2/lodash.min'
	},

	shim: {
		Backbone: {
			deps: ['Underscore', 'jQuery'],
			exports: 'Backbone'
		},
		Facebook: {
			exports: 'FB'
		},
		Handlebars: {
			exports: 'Handlebars'
		},
		jQuery: {
			exports: 'jQuery'
		},
		Underscore: {
			exports: '_'
		},
		'plugins/backbone.layoutmanager': ['Backbone']
	},

	waitSeconds: 20

});
