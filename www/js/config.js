require.config({

	baseUrl: 'js',

	deps: ['main'],

	paths: {
		Backbone: '//cdnjs.cloudflare.com/ajax/libs/backbone.js/0.9.2/backbone-min',
		GoogleAnalytics: 'libs/google-analytics',
		jQuery: '//cdnjs.cloudflare.com/ajax/libs/jquery/1.7.2/jquery.min',
		Mustache: '//cdnjs.cloudflare.com/ajax/libs/mustache.js/0.5.0-dev/mustache.min',
		Underscore: '//cdnjs.cloudflare.com/ajax/libs/lodash.js/0.3.2/lodash.min'
	},

	shim: {
		Backbone: {
			deps: ['Underscore', 'jQuery'],
			exports: 'Backbone'
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
	}
});
