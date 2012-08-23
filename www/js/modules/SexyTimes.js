define(['jQuery', 'Underscore', 'Backbone', 'app',
	'Chosen',
	'modules/Dummy',
	'modules/Popup'
],
function($, _, Backbone, app,
	Chosen,
	Dummy,
	Popup
) {

	var Collections = {},
		Views = {};

	var Model = Backbone.Model.extend({
	});

	Collections.Upcoming = Backbone.Collection.extend({
		model: Model,
		url: function () {
			return app.api + 'activities/sexytimes/upcoming/';
		},
		parse: function (response) {
			return response.sexytimes;
		},
		dummy: function () {
			this.reset(Dummy.getSexyTimes());
		}
	});

	Views.Upcoming = Backbone.View.extend({
		template: 'sexytimes/upcoming',
		initialize: function () {
			this.collection.on('reset', this.render, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return {sexyTimes: this.collection.toJSON()};
		},
		events: {
			'click .create-sexytime': function (event) {
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

	Views.Menu = Backbone.View.extend({
		template: 'sexytimes/menu',
		initialize: function () {
			this.collection.on('reset', this.render, this);
		},
		cleanup: function () {
			this.collection.off(null, null, this);
		},
		serialize: function () {
			return {sexyTimes: this.collection.toJSON()};
		}
	});

	Views.Create = Popup.extend({
		template: 'sexytimes/create',
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
		Model: Model,
		Collections: Collections,
		Views: Views
	};
});
