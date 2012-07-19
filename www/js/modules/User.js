define(['jQuery', 'Underscore', 'Mustache', 'Backbone', 'app'],
function($, _, Mustache, Backbone, app) {

	var Views = {};

	var Model = Backbone.Model.extend({
		initialize: function(models, options) {
		}
	});

	var Collection = Backbone.Collection.extend({
	});


	/*
	 * DEFINITION OF VIEWS
	 */
	

	// My Full User Profile
	Views.MyFullProfile = Backbone.View.extend({
		template: 'user/profile',
		render: function (manage) {
			return manage(this).render(this.model.toJSON());
		}
	});

	// Friend Full User Profile
	Views.FriendFullProfile = Backbone.View.extend({
		template: 'user/profile-friend',
		render: function (manage) {
			return manage(this).render(this.model.toJSON());
		}
	});

	// FOF Full User Profile
	Views.FofFullProfile = Backbone.View.extend({
		template: 'user/profile-fof',
		render: function (manage) {
			return manage(this).render(this.model.toJSON());
		}
	});


	// Medium User: Profile image, name and more information
	Views.Medium = Backbone.View.extend({
		template: 'user/medium',
		tagName: 'li',
//		serialize: function () {return this.model.toJSON();}
	});


	// Small User: Profile image and name
	Views.Small = Backbone.View.extend({
		template: 'user/small',
		tagName: 'li',
//		serialize: function () {return this.model.toJSON();}
	});


	// SexyTime (Date) User: Profile image and date invitation text
	Views.SexyTime = Backbone.View.extend({
		template: 'user/sexytime',
		tagName: 'li',
//		serialize: function () {return this.model.toJSON();}
	});


	// Points User: Profile image, name and points
	Views.Points = Backbone.View.extend({
		template: 'user/points',
		tagName: 'li',
//		serialize: function () {return this.model.toJSON();}
	});
	
	
	// Tiny User: Only the profile image
	Views.Tiny = Backbone.View.extend({
		template: 'user/tiny',
		tagName: 'li',
		serialize: function () {
			return this.model.toJSON();
		}
	});

	return {
		Model: Model,
		Collection: Collection,
		Views: Views
	};
});