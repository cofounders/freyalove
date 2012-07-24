define(['jQuery', 'Underscore', 'Backbone', 'app', 'modules/User'],
function($, _, Backbone, app, User) {

	var Collections = {},
		Views = {};

	var Model = Backbone.Model.extend({
		initialize: function(models, options) {
		}
	});

	Collections.FacebookFriends = Backbone.Collection.extend({
		model: Model,
/*
		fetch: function () {
			console.log('[FAKE] FETCHING FB FRIENDS');
			var that = this;
			setTimeout(function () {
				that.reset(app.friends);
			}, 100);
		},
*/
		url: function () {
			return app.api + 'users/' + (this.options.id || 4) + '/facebookfriends/';
		},

		initialize: function(models, options) {
			this.options = options || {};
		}
	});

	Collections.Friends = Backbone.Collection.extend({
		
		// checks if e is in this collection
		indexOf: function (e) {
			var i = 0;
			for (; i < this.length; i++) {
				if (this.models[i].id == e.id)
					return i;
			}
			return -1;
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
				this.insertView('ul.bblm-friends-list', new User.Views.Tiny({
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

	// Friend list on the right hand friend panel
	Views.ListWinks = Backbone.View.extend({
//		template: 'friends/list-right',

		render: function (manage) {
			this.collection.each(function (user) {
				this.insertView('ul', new User.Views.Small({
					model: user
				}));
			}, this);
			return manage(this).render();
		}
	});


	return {
		Model: Model,
		Collections: Collections,
		Views: Views
	};
});
