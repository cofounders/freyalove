define(['Underscore', 'Backbone'],
function(_, Backbone) {
	return Backbone.Model.extend({
		url: function () {
			return 'Backbone.Session';
		},
		initialize: function (properties, options) {
			this.options = options || {};
			this.fetch();
		},
		sync: function (method, model, options) {
			options = options || {};
			var url = this.options.url || this.url,
				key = _.isFunction(url) ? url() : '' + url,
				response;
			switch (method) {
				case 'create':
				case 'update':
					response = sessionStorage.setItem(key, JSON.stringify(this.toJSON()));
					break;
				case 'delete':
					response = sessionStorage.removeItem(key);
					break;
				case 'read':
					response = JSON.parse(sessionStorage.getItem(key));
					break;
			}
			if (_.isFunction(options.success)) { options.success(response); }
		},
		signIn: function (options) {
			options = options || {};
			console.log('Override the signIn method');
			if (_.isFunction(options.error)) options.error(this);
		},
		signOut: function (options) {
			options = options || {};
			this.destroy();
			this.clear();
			this.trigger('signOut');
			if (_.isFunction(options.success)) options.success(this);
		},
		getAuthStatus: function (options) {
			options = options || {};
			console.log('Override the getAuthStatus method');
			if (_.isFunction(options.error)) options.error(this);
		}
	});
});
