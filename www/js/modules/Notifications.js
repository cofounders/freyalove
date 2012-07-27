define(['jQuery', 'Underscore', 'Backbone', 'app', 'modules/Dummy'],
function($, _, Backbone, app, Dummy) {
	var Collections = {},
		Views = {};

	var Model = Backbone.Model.extend({
	});

	Collections.Recent = Backbone.Collection.extend({
		model: Model,
		url: function () {
			return app.api + 'notifications/unread/';
		},
		parse: function (response) {
			var types = app.constants.NOTIFICATION_TYPE,
				typeById = _.reduce(types, function (result, value, key) {
					result[value] = key;
					return result;
				}, {});
			return _.map(response.notifications || [], function (notification) {
				var label = typeById[notification.type];
				notification[label] = true;
				return notification;
			});
		},
		fetch: function () {
			this.reset(Dummy.getNotifications());
		}
	});

	Views.Menu = Backbone.View.extend({
		template: 'notifications/menu',
		initialize: function () {
			this.collection.on('reset', function () {
				this.render();
			}, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return {notifications: this.collection.toJSON()};
		}
	});

	return {
		Model: Model,
		Collections: Collections,
		Views: Views
	};
});
