define([], function () {
	return function (url, params) {
		var param = /:[\w\-\d]+/i;
		return url.replace(param, function (match) {
			var name = match.substr(1),
				data = params[name];
			return encodeURIComponent(data);
		});
	};
});