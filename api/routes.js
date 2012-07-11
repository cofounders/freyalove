var mongoose = require('mongoose'),
	app = require('./app'),
	models = require('./models');

app.server.get('/user/:userId', function (req, res, next) {
	res.send({
		userId: req.params.userId
	});
	return next();
});
