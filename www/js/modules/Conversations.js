define(['jQuery', 'Underscore', 'Backbone', 'app', 'modules/Dummy'],
function($, _, Backbone, app, Dummy) {
	var Collections = {},
		Views = {};

	var Model = Backbone.Model.extend({
	});

	Collections.Recent = Backbone.Collection.extend({
		model: Model,
		url: function () {
			return app.api + 'conversations/';
		},
		parse: function (response) {
			var types = app.constants.CONVERSATION_STATUS,
				typeById = _.reduce(types, function (result, value, key) {
					result[value] = key;
					return result;
				}, {});
			return _.map(response.conversations || [], function (conversation) {
				var label = typeById[conversation.status];
				conversation[label] = true;
				return conversation;
			});
		},
		fetch: function () {
			this.reset(Dummy.getMessages());
		}
	});

	Views.Menu = Backbone.View.extend({
		template: 'conversations/menu',
		initialize: function () {
			this.collection.on('reset', function () {
				this.render();
			}, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return {conversations: this.collection.toJSON()};
		}
	});

	return {
		Model: Model,
		Collections: Collections,
		Views: Views
	};
});
