define(['Underscore', 'Backbone'],
function(_, Backbone) {
	return Backbone.Model.extend({
		initialize: function (properties, options) {
			this.fetch();
		},
		sync: function (method, model, options) {
			var storageKey = 'Backbone.Session',
				response;
			switch (method) {
				case 'create':
				case 'update':
					response = sessionStorage.setItem(storageKey, JSON.stringify(this.toJSON()));
					break;
				case 'delete':
					response = sessionStorage.removeItem(storageKey);
					break;
				case 'read':
					response = JSON.parse(sessionStorage.getItem(storageKey));
					break;
			}
			if (_.isFunction(options.success)) { options.success(response); }
		},
		signIn: function (options) {
			console.log('Override the signIn method');
			if (_.isFunction(options.error)) options.error(this);
		},
		signOut: function (options) {
			this.destroy();
			this.clear();
			if (_.isFunction(options.success)) options.success(this);
		},
		getAuthStatus: function (options) {
			console.log('Override the getAuthStatus method');
			if (_.isFunction(options.error)) options.error(this);
		}
	});
});
