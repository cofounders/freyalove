define(['Underscore', 'Facebook', 'modules/Session/Base'],
function(_, Facebook, Session) {
	return Session.extend({
		signIn: function (options) {
			Facebook.login(_.bind(function(response) {
				if (response.authResponse) {
					this.save({id: response.authResponse.userID}, options);
				} else {
					options.error();
				}
			}, this));
		},
		getAuthStatus: function (options) {
			Facebook.getLoginStatus(_.bind(function(response) {
				if (response.status === 'connected') {
					options.success();
				} else {
					options.error();
				}
			}, this));
		}
	});
});
