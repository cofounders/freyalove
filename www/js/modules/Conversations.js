define(['jQuery', 'Underscore', 'Backbone', 'app',
	'modules/Friends',
	'modules/Dummy'
],
function($, _, Backbone, app,
	Friends,
	Dummy
) {
	var Models = {},
		Collections = {},
		Views = {};

	var types = app.constants.CONVERSATION_STATUS,
		typeById = _.reduce(types, function (result, value, key) {
			result[value] = key;
			return result;
		}, {}),
		checkType = function (response) {
			return _.map(response.conversations || [], function (conversation) {
				var label = typeById[conversation.status];
				conversation[label] = true;
				return conversation;
			});
		};

	Models.Conversation = Backbone.Model.extend({
	});

	Models.ConversationSummary = Backbone.Model.extend({
	});

	Models.Message = Backbone.Model.extend({
	});

	Collections.Recent = Backbone.Collection.extend({
		model: Models.ConversationSummary,
		url: function () {
			return app.api + 'conversations/';
		},
		parse: checkType,
		fetch: function () {
			this.reset(Dummy.getMessages());
		}
	});

	Collections.Conversation = Backbone.Collection.extend({
		model: Models.Message,
		initialize: function (models, options) {
			this.options = _.extend({
				to: new Friends.Models.UserSummary(),
			}, options);
		},
		url: function () {
			return app.api + 'conversations/' + this.options.to.id + '/messages/';
		},
		parse: checkType,
		fetch: function () {
			this.reset(Dummy.getMessages());
		}
	});

	Views.Conversation = Backbone.View.extend({
		template: 'conversations/conversation',
		initialize: function () {
			this.collection.on('reset', this.render, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return {messages: this.collection.toJSON()};
		}
	});

	Views.Menu = Backbone.View.extend({
		template: 'conversations/menu',
		initialize: function () {
			this.collection.on('reset', this.render, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return {conversations: this.collection.toJSON()};
		}
	});

	Views.Recent = Backbone.View.extend({
		template: 'conversations/recent',
		initialize: function () {
			this.collection.on('reset', this.render, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return {conversations: this.collection.toJSON()};
		}
	});

	return {
		Models: Models,
		Collections: Collections,
		Views: Views
	};
});
