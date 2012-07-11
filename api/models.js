var mongoose = require('mongoose'),
	schema = function (props) { return new mongoose.Schema(props); },
	model = function (name, schema) { return mongoose.model(name, schema); },
	define = function (name, props) { exports[name] = model(name, schema(props)); };

define('User', {
	name: String,
	email: String,
	facebookId: String
});
