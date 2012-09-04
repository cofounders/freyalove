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

	var Collections = {},
		Views = {};

	var Model = Backbone.Model.extend({
	});

	Collections.Upcoming = Backbone.Collection.extend({
		model: Model,
		url: function () {
			return app.api + 'activities/sexytimes/upcoming/';
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

				var popup = new Views.Create({
					collection: new Friends.Collections.All()
				});
				app.layout.insertViews({
					'.bblm-popup': popup
				});
				// popup.render();
				popup.collection.fetch();

			}
		}
	});

	Views.Menu = Views.Upcoming.extend({
		template: 'sexytimes/menu'
	});

	Views.Create = Popup.extend({
		template: 'sexytimes/create',
		serialize: function () {
			return {
				count: this.collection.length,
				friends: this.collection.toJSON()
			};
		},
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
