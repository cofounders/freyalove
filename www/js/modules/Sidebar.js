define(['jQuery', 'Underscore', 'Backbone', 'app',
	'modules/SexyTimes',
	'modules/Friends',
	'modules/Activities',
	'modules/Matchmakers'
],
function($, _, Backbone, app,
	SexyTimes,
	Friends,
	Activities,
	Matchmakers
) {
	var Views = {};

	Views.Panels = Backbone.View.extend({
		template: 'sidebar/panels',
		render: function (manage) {

			var commonFriends = new Friends.Collections.Common();
			this.insertView('.bblm-friends-common', new Friends.Views.Common({
				collection: commonFriends
			}));
			commonFriends.fetch();

			var upcomingSexyTimes = new SexyTimes.Collections.Upcoming();
			this.insertView('.bblm-sexytimes-upcoming', new SexyTimes.Views.Upcoming({
				collection: upcomingSexyTimes
			}));
			upcomingSexyTimes.fetch();

			var allFriends = new Friends.Collections.All();
			this.insertView('.bblm-friends-all', new Friends.Views.All({
				collection: allFriends
			}));
			allFriends.fetch();

			var recentActivities = new Activities.Collections.Recent();
			this.insertView('.bblm-activities-recent', new Activities.Views.Recent({
				collection: recentActivities
			}));
			recentActivities.fetch();

			var topMatchmakers = new Matchmakers.Collections.Top();
			this.insertView('.bblm-matchmakers-top', new Matchmakers.Views.Top({
				collection: topMatchmakers
			}));
			topMatchmakers.fetch();

			return manage(this).render();
		}
	});

	return {
		Views: Views
	};
});
