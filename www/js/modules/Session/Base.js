define(['Underscore', 'Backbone', 'libs/localStorage'],
function(_, Backbone, localStorage) {
	return Backbone.Model.extend({
		initialize: function (properties, options) {
			this.options = options || {};
			this.fetch();
		},
		getAuthStatus: function (options) {
			options = options || {};
			console.log('Backbone.Session: Override the getAuthStatus method');
			if (_.isFunction(options.error)) options.error(this);
		},
		signIn: function (options) {
			options = options || {};
			console.log('Backbone.Session: Override the signIn method');
			if (_.isFunction(options.error)) options.error(this);
		},
		signOut: function (options) {
			options = options || {};
			this.destroy();
			this.clear();
			this.trigger('signOut');
			if (_.isFunction(options.success)) options.success(this);
		},
		sync: function (method, model, options) {
			options = options || {};
			var url = this.options.url || this.url,
				key = _.isFunction(url) ? url() : '' + url,
				response;
			switch (method) {
				case 'create':
				case 'update':
					response = localStorage.setItem(key, JSON.stringify(this.toJSON()));
					break;
				case 'delete':
					response = localStorage.removeItem(key);
					break;
				case 'read':
					response = JSON.parse(localStorage.getItem(key) || null);
					break;
			}
			if (_.isFunction(options.success)) { options.success(response); }
		},
		url: function () {
			return 'Backbone.Session';
		}
	});
});