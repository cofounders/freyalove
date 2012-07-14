define(['Facebook'], function () {

	Facebook.init({
/* */
		appId      : '415866361791508', // App ID
		channelUrl : '//freyalove.cofounders.sg/channel.html', // Channel File
		status     : false, // check login status
		cookie     : true, // enable cookies to allow the server to access the session
		xfbml      : false  // parse XFBML
/* */
	});
	Facebook.Event.subscribe('auth.authResponseChange', function (response) {
		console.log('[auth.authResponseChange] The status of the session is: ' + response.status);
		if (response.status === 'connected') {
			user.loggedIn = true;
			Backbone.history.navigate('/dashboard', true);
		}
	});
	Facebook.Event.subscribe('auth.login', function (response) {
		console.log('[auth.login] The status of the session is: ' + response.status);
		user.loggedIn = true;
		Backbone.history.navigate('/dashboard', true);
	});

	var user = _.extend({
		loggedIn: false;
	}, Backbone.Events);

	return user;
});
