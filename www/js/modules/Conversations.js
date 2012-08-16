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
		checkType = function (conversations) {
			return _.map(conversations || [], function (conversation) {
				var label = typeById[conversation.status];
				conversation[label] = true;
				return conversation;
			});
		};

	Models.Conversation = Backbone.Model.extend({
		initialize: function (options) {
			this.options = _.extend({
				to: new Friends.Models.UserSummary()
			}, options);
		},
		url: function () {
			return app.api + 'conversations/with/' + this.options.to.id + '/';
		},
		parse: function (response) {
			response.messages = checkType(response.messages);
			return response;
		},
		dummy: function () {
			var conversation = Dummy.getConversation();
			conversation.participants[0].id = app.session.id;
			this.set(this.parse(conversation));
		}
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
		dummy: function () {
			this.reset(this.parse(Dummy.getMessages()));
		}
	});

	Views.Conversation = Backbone.View.extend({
		template: 'conversations/conversation',
		initialize: function () {
			this.model.on('change', this.render, this);
		},
		cleanup: function () {
			this.model.off(null, null, this);
		},
		serialize: function () {
			var context = this.model.toJSON(),
				someoneElse = function (participant) {
					return participant.id !== app.session.id;
				};
			context.participants = _.filter(context.participants, someoneElse);
			context.messages = (context.messages || []).concat().reverse();
			return context;
		},
		events: {
			"submit form": "sendMessage"
		},
		sendMessage: function (event) {
			event.stopPropagation();
			event.preventDefault();

			var body = this.$('textarea').val(),
				url = app.api + '/conversations/message/',
				participants = _.pluck(this.model.get('participants'), 'id');

			this.$('textarea').val('');

			$.post(url, {
				to: participants,
				body: body
			}, function (data, textStatus, jqXHR) {
			});
		}
		// render: function (manage) {
		// 	setTimeout( function () {
		// 		var height = $(".conversation-viewport > ol").height();
		// 		$(".conversation-viewport").scrollTop(height);
		// 	}, 500);
		// 	return manage(this).render();
		// }
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
			return {
				conversations: this.collection.toJSON()
			};
		}
	});

	return {
		Models: Models,
		Collections: Collections,
		Views: Views
	};
});
