var mongoose = require('mongoose'),
	schema = function (props) { return new mongoose.Schema(props); },
	model = function (name, schema) { return mongoose.model(name, schema); },
	define = function (name, props) { exports[name] = model(name, schema(props)); };

define('User', {
	name: String,
	email: String,
	facebookId: String
});

console.log('user', mongoose.model('User').schema);

define('UserSummary', {
});

define('Activity', {
});

// inherit Activity
define('Match', {
});

// inherit Match
define('SexyTime', {
});

// inherit Activity
define('Wink', {
});

define('MatchProposal', {
});

define('Note', {
});

define('Message', {
});

define('Conversation', {
});

define('ConversationSummary', {
});

define('FacebookFriends', {
});

define('PrivacySetting', {
});

define('Question', {
});

define('Answer', {
});
