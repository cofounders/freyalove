var _ = require('lodash'),
	restify = require('restify'),
	mongoose = require('mongoose'),
	config = require('./config');

var db = mongoose.connect(config.credentials.mongodb);

var server = restify.createServer({
	name: config.rest.name,
	version: config.rest.version
});
server.use(restify.bodyParser({
	mapParams: false
}));
server.listen(config.rest.port, config.rest.host, function () {
	console.log('%s listening at %s', server.name, server.url);
});

_.extend(exports, {
	server: server,
	db: db
});
