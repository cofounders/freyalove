define(['Underscore', 'Facebook', 'modules/Session/Base'],
function(_, Facebook, Session) {
	return Session.extend({
		signIn: function (options) {
			Facebook.login(_.bind(function(response) {
				if (response.authResponse) {
					this.save({id: response.authResponse.userID});
					Facebook.api('/me', _.bind(function (response) {
						if (response && !response.error) {
							this.save({
								email: response.email,
								name: response.name,
								username: response.username
							}, options);
						} else {
							return options.error();
						}
					}, this));
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
