define(['jQuery', 'Underscore', 'Mustache', 'Backbone', 'app'],
function($, _, Mustache, Backbone, app) {
	return {

		Model: Backbone.Model.extend({
			defaults: {firstname: "Bette", lastname: "Porter", age: 35}
		}),

		Collection: Backbone.Collection.extend({
		}),

		Views: {

			LeaderboardTop: Backbone.View.extend({
				template: 'friends/leaderboard-top'
			}),

			LeaderboardFull: Backbone.View.extend({
				template: 'friends/leaderboard-full'
			}),

			ListRight: Backbone.View.extend({
				template: 'friends/list-right'
			}),

			ListRightCommon: Backbone.View.extend({
				template: 'friends/list-right-common'
			}),

			UpcomingDates: Backbone.View.extend({
				template: 'friends/dates-upcoming'
			})

		}

	};
});