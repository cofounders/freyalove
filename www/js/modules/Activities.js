define(['jQuery', 'Underscore', 'Backbone', 'app', 'modules/Dummy'],
function($, _, Backbone, app, Dummy) {
	var Collections = {},
		Views = {};

	var Model = Backbone.Model.extend({
	});

	Collections.Recent = Backbone.Collection.extend({
		model: Model,
		url: function () {
			return app.api + 'activities/';
		},
		parse: function (response) {
			var types = app.constants.ACTIVITY_TYPE,
				typeById = _.reduce(types, function (result, value, key) {
					result[value] = key;
					return result;
				}, {});
			return _.map(response.activities || [], function (activity) {
				var label = typeById[activity.type];
				activity[label] = true;
				return activity;
			});
		},
		fetch: function () {
			this.reset(Dummy.getRecentActivities());
		}
	});

	Views.Recent = Backbone.View.extend({
		template: 'activities/recent',
		initialize: function () {
			this.collection.on('reset', function () {
				this.render();
			}, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return {activities: this.collection.toJSON()};
		}
	});

	return {
		Model: Model,
		Collections: Collections,
		Views: Views
	};
});
