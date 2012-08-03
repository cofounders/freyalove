define(['jQuery', 'Underscore', 'Backbone', 'app', 'modules/Dummy'],
function($, _, Backbone, app, Dummy) {
	var interval;
	return Backbone.Model.extend({
		timer: 30000,
		go: function () {
			clearInterval(interval);
			interval = setInterval(_.bind(this.fetch, this), this.timer);
			this.fetch();
		},
		pause: function () {
			clearInterval(interval);
		},
		url: function () {
			return app.api + 'stream/unread';
		},
		parse: function (response) {
			return response.unread;
		},
		fetch: function () {
			this.set(Dummy.getStreamUnread());
		}
	});
});
