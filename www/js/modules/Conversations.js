define(['jQuery', 'Underscore', 'Backbone', 'app',
	'Chosen',
	'modules/Dummy',
	'modules/Friends',
	'modules/Popup'
],
function($, _, Backbone, app,
	Chosen,
	Dummy,
	Friends,
	Popup
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
			return {conversations: this.collection.toJSON().slice(0, 4)};
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
		},
		events: {
			'click .button.create-conversation': function (event) {
				event.stopPropagation();
				event.preventDefault();

				var popup = new Views.Create();
				app.layout.insertViews({
					'.bblm-popup': popup
				});
				popup.render();
			}
		}
	});

	Views.Create = Popup.extend({
		template: 'conversations/create',
		events: {
			'click .close': function (event) {
				event.stopPropagation();
				event.preventDefault();
				this.remove();
			}
		},
		render: function (manage) {
			var deferred = manage(this).render();
			deferred.then(_.bind(function () {
				this.$('select').chosen();
			}, this));
			return deferred;
		}
	});

	return {
		Models: Models,
		Collections: Collections,
		Views: Views
	};
});
