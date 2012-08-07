define(['Underscore', 'Backbone'], function (_, Backbone) {
	var api = {},
		active = false,
		originalSync = Backbone.sync;

	Backbone.sync = function (method, model, options) {
		return active && _.isFunction(model.dummy)
			? model.dummy.apply(this, arguments)
			: originalSync.apply(this, arguments);
	};

	Object.defineProperty(api, 'intercept', {
		get: function () { return active; },
		set: function (value) { active = !!value; }
	});

	return api;
});
