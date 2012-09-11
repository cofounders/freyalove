define(['Underscore'], function (_) {
	return function (url, params, options) {
		var label = /:[\w\-\d]+/i;
		_.extend({
			separator: '+'
		}, options);
		return url.replace(label, function (match) {
			var name = match.substr(1),
				param = params[name];
			return _.isArray(param) ? _.map(param, encodeURIComponent).join(options.separator)
				: _.isFunction(param) ? encodeURIComponent(param())
				: encodeURIComponent(param);
		});
	};
});