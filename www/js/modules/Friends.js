define(['jQuery', 'Underscore', 'Mustache', 'Backbone', 'app', 'modules/UserPreview'],
function($, _, Mustache, Backbone, app, UserPreview) {

	var Views = {};

	var Model = Backbone.Model.extend({
		initialize: function(models, options) {
		}
	});

	var Collection = Backbone.Collection.extend({
		model: Model,

		fetch: function () {
			console.log('[FAKE] FETCHING FB FRIENDS');
			var that = this;
			setTimeout(function () {
				that.reset(app.friends);
			}, 100);
		},

		url: function () {
			return app.api + 'users/' + this.options.userId + '/facebookfriends/';
		},

		initialize: function(models, options) {
			this.options = options || {};
		}
	});



	// VIEWS


	Views.LeaderboardTop = Backbone.View.extend({
		template: 'friends/leaderboard-top'
	});



	Views.LeaderboardFull = Backbone.View.extend({
		template: 'friends/leaderboard-full'
	});
	
	
	// Friend list on the right hand friend panel
	Views.ListRight = Backbone.View.extend({
		template: 'friends/list-right',

		initialize: function () {
			this.collection.on('reset', this.render, this);

			// this.collection.on('fetch', function () {
			// 	this.$el.html('<img src="'"/assets/img/spinner.gif">'');
			// }, this);
		},

		render: function (manage) {
			this.collection.each(function (user) {
				this.insertView('ul', new UserPreview.Views.Tiny({
					model: user
				}));
			}, this);
			return manage(this).render();
		}
	});


	Views.ListRightCommon = Backbone.View.extend({
		template: 'friends/list-right-common'
	});

	Views.UpcomingDates = Backbone.View.extend({
		template: 'friends/dates-upcoming'
	});

	return {
		Model: Model,
		Collection: Collection,
		Views: Views
	};
});
