require.config({

	baseUrl: '/js',

	deps: ['main'],

	paths: {
		Backbone: '//cdnjs.cloudflare.com/ajax/libs/backbone.js/0.9.2/backbone-min',
		Chosen: 'plugins/chosen.jquery',
		Facebook: '//connect.facebook.net/en_US/all',
		jQuery: '//cdnjs.cloudflare.com/ajax/libs/jquery/1.8.0/jquery-1.8.0.min',
		Mustache: '//cdnjs.cloudflare.com/ajax/libs/mustache.js/0.5.0-dev/mustache.min',
		Underscore: '//cdnjs.cloudflare.com/ajax/libs/lodash.js/0.3.2/lodash.min'
	},

	shim: {
		Backbone: {
			deps: ['Underscore', 'jQuery'],
			exports: 'Backbone'
		},
		Chosen: {
			deps: ['jQuery'],
			exports: 'jQuery'
		},
		Facebook: {
			exports: 'FB'
		},
		jQuery: {
			exports: 'jQuery'
		},
		Mustache: {
			exports: 'Mustache'
		},
		Underscore: {
			exports: '_'
		},
		'plugins/backbone.layoutmanager': ['Backbone']
	},

	waitSeconds: 20

});
