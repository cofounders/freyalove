define(['Underscore', 'Facebook', 'modules/Session/Base'],
function(_, Facebook, Session) {
	return Session.extend({
		signIn: function (options) {
			options = options || {};
			Facebook.login(_.bind(function(response) {
				if (response.authResponse) {
					this.save({userID: response.authResponse.userID}, {
						error: options.error,
						success: _.bind(function () {
							this.trigger('signIn');
							if (_.isFunction(options.success)) options.success();
						}, this)
					});
				} else {
					if (_.isFunction(options.error)) options.error();
				}
			}, this));
		},
		getAuthStatus: function (options) {
			options = options || {};
			Facebook.getLoginStatus(_.bind(function(response) {
				if (response.status === 'connected') {
					if (_.isFunction(options.success)) options.success();
				} else {
					if (_.isFunction(options.error)) options.error();
				}
			}, this));
		}
	});
});
