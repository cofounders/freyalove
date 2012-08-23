define(['jQuery', 'Underscore', 'Backbone', 'app',
	'modules/Conversations',
	'modules/Notifications',
	'modules/SexyTimes',
],
function($, _, Backbone, app,
	Conversations,
	Notifications,
	SexyTimes
) {
	var Views = {};

	var activeMenuView = null;

	var cleanupMenu = function () {
		if (activeMenuView) {
			// $(activeMenuView.el).closest('.opened').removeClass('opened');
			$(this.el).find('section.opened').removeClass('opened');

			// activeMenuView.removeView();
			// activeMenuView.remove();

			// this.remove();
			this.removeView();

			activeMenuView = null;
		}
	};

	Views.Menu = Backbone.View.extend({
		template: 'header/menu',
		initialize: function (options) {
			app.stream.on('change', function () {
				app.stream.get('unreadNotifications')
					? $(this.el).find('.notifications').attr('data-unread', app.stream.get('unreadNotifications'))
					: $(this.el).find('.notifications').removeAttr('data-unread');
				app.stream.get('unreadConversations')
					? $(this.el).find('.conversations').attr('data-unread', app.stream.get('unreadConversations'))
					: $(this.el).find('.conversations').removeAttr('data-unread');
				app.stream.get('unreadSexyTimes')
					? $(this.el).find('.sexytimes').attr('data-unread', app.stream.get('unreadSexyTimes'))
					: $(this.el).find('.sexytimes').removeAttr('data-unread');
			}, this);
			app.session.on('change:name', function () {
				$(this.el).find('.name')
					.text(app.session.get('name'))
					.attr('href', '/profile/' + app.session.get('id'));
			}, this);
			$(document).on('click', this.closeMenu = _.bind(this.closeMenu, this));
		},
		closeMenu: function (event) {
			var menu = $(this.el).find('menu').get(0),
				clickedInsideMenu = $.contains(menu, event.target);
			if (activeMenuView && !clickedInsideMenu) {
				cleanupMenu.call(this);
			}
		},
		cleanup: function () {
			app.stream.off(null, null, this);
			app.session.off(null, null, this);
			$(document).off('click', this.closeMenu);
		},
		serialize: function () {
			return _.extend(
				app.session.toJSON(),
				app.stream.toJSON()
			);
		},
		events: {
			'submit nav > form.search': function (event) {
				event.stopPropagation();
				event.preventDefault();
				var query = $(this.el).find('input[name="query"]').val();
				Backbone.history.navigate('/search/' + encodeURIComponent(query), true);
			},
			'click .signout': function (event) {
				event.stopPropagation();
				event.preventDefault();
				app.session.signOut();
			},
			'click nav > menu > li > a': function (event) {
				event.stopPropagation();
				event.preventDefault();
				var menus = {
						notifications: {
							collection: Notifications.Collections.Recent,
							view: Notifications.Views.Menu,
							unread: 'unreadNotifications'
						},
						conversations: {
							collection: Conversations.Collections.Recent,
							view: Conversations.Views.Menu,
							unread: 'unreadConversations'
						},
						sexytimes: {
							collection: SexyTimes.Collections.Upcoming,
							view: SexyTimes.Views.Menu,
							unread: 'unreadSexyTimes'
						}
					},
					el = $(event.target).next('section'),
					section = $(event.target).attr('class'),
					data = new menus[section].collection(),
					selector = '.' + section + ' + section';

				if (activeMenuView) {
					cleanupMenu.call(this);
				}

				activeMenuView = new menus[section].view({
					collection: data
				});

				app.stream.set(menus[section].unread, 0);

				this.setView(selector, activeMenuView);
				activeMenuView.render();
				el.addClass('opened');
				data.fetch();
			}
		}
	});

	Views.Public = Backbone.View.extend({
		template: 'header/public',
		events: {
			'click .button.facebook': function (event) {
				event.stopPropagation();
				event.preventDefault();
				app.session.signIn({scope: 'email,user_likes'});
			}
		}
	});

	return {
		Views: Views
	};
});
