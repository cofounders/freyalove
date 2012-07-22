define(['Underscore', 'Facebook', 'modules/Session/Base'],
function(_, Facebook, Session) {
	return Session.extend({
		signIn: function (options) {
			options = options || {};
			var that = this,
				authResponse = Facebook.getAuthResponse(),
				onSuccess = function (authResponse) {
					that.save(authResponse, {
						error: options.error,
						success: function () {
							that.trigger('signIn');
							if (_.isFunction(options.success)) options.success();
						}
					});
				};
			if (authResponse) {
				onSuccess(authResponse);
			} else {
				Facebook.login(function (response) {
					if (response.authResponse) {
						onSuccess(response.authResponse);
					} else {
						if (_.isFunction(options.error)) options.error();
					}
				});
			}
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
