define(['jQuery', 'Underscore', 'Backbone', 'app', 'modules/Dummy'],
function($, _, Backbone, app, Dummy) {

	var Tabs = [],
		Views = {};

	Views.Likes = Backbone.View.extend({
		template: 'friends/tab/likes'
	});

	Views.Quotes = Backbone.View.extend({
		template: 'friends/tab/quotes'
	});

	Views.About = Backbone.View.extend({
		template: 'friends/tab/about'
	});

	Views.Looks = Backbone.View.extend({
		template: 'friends/tab/looks'
	});

	Views.Lifestyle = Backbone.View.extend({
		template: 'friends/tab/lifestyle'
	});

	Views.Relationship = Backbone.View.extend({
		template: 'friends/tab/relationship'
	});

	Views.Background = Backbone.View.extend({
		template: 'friends/tab/background'
	});

	Views.Personality = Backbone.View.extend({
		template: 'friends/tab/personality'
	});

	Views.Sexuality = Backbone.View.extend({
		template: 'friends/tab/sexuality'
	});

	Tabs = [
		{
			name: 'Likes',
			view: Views.Likes
		},
		{
			name: 'Favorite Quotes',
			view: Views.Quotes
		},
		{
			name: 'Questionnaire',
			view: Views.About,
			tabs: [
				{
					name: 'About',
					view: Views.About
				},
				{
					name: 'Looks',
					view: Views.Looks
				},
				{
					name: 'Lifestyle',
					view: Views.Lifestyle
				},
				{
					name: 'Relationship',
					view: Views.Relationship
				},
				{
					name: 'Background',
					view: Views.Background
				},
				{
					name: 'Personality',
					view: Views.Personality
				},
				{
					name: 'Sexuality',
					view: Views.Sexuality
				}
			]
		}
	];

	return {
		Tabs: Tabs,
		Views: Views
	};
});
