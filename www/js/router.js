define([
	'app'
], function (app) {
	return Backbone.Router.extend({

		routes: {
			'': 'index'
		},

		index: function () {
			console.log("Default landing page");
		}

	});
});
