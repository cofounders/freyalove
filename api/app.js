var _ = require('lodash'),
	config = require('./config'),
	everyauth = require('everyauth'),
	express = require('express'),
	mongoose = require('mongoose');

var db = mongoose.connect(config.credentials.mongodb);

var server = express.createServer({
	name: config.rest.name,
	version: config.rest.version
});
server.use(express.bodyParser({
	mapParams: false
}));
server.listen(config.rest.port, config.rest.host, function () {
	console.log('%s listening at %s', server.name, server.url);
});

_.extend(exports, {
	server: server,
	db: db
});
