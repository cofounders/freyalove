define([], function () {

// FRIENDS
	// DIRECT FRIENDS
	var user0 = {"firstName": "Sebastiaan"
	,"lastName": "Deckers"
	,"dateOfBirth": "09/05/1983"
	,"about": "Lorem Ipsum Rockstar"
	,"id": 1
	,"profileImage": "/dummy/user2.png"};
	
	var user1 = {"firstName": "Wolf"
	,"lastName": "Maehr"
	,"dateOfBirth": "09/05/1973"
	,"about": "UX Lorem Ipsum Rockstar"
	,"id": 2
	,"profileImage": "/dummy/user3.png"};
	
	var user2 = {"firstName": "Veron"
	,"lastName": "Boobs"
	,"dateOfBirth": "09/05/1988"
	,"about": "Lorem Ipsum Tits"
	,"id": 3
	,"profileImage": "/dummy/user1.png"};
	
	var user3 = {"firstName": "Sayanee"
	,"lastName": "Basu"
	,"dateOfBirth": "09/08/1983"
	,"about": "That's not even cleavage!"
	,"id": 4
	,"profileImage": "/dummy/user0.png"};
	
	// FRIENDS OF FRIENDS
	
	
	
	var allUsers = [user0, user1, user2, user3, user10, user11, user12, user12, user14, user20, user21, user22];
	var allProfiles = [user0, user1, user2, user3, user10, user11, user12, user12, user14];
	var allFriends = [user0, user1, user2, user3];
		
	return {

	// USERS
		getAllUsers: function() {
			return allUsers;
		},

		getMyProfile: function () {
			return user0;
		},
		
		getRandomProfile: function() {
			return [allUsers[Math.floor((Math.random()*allUsers.length))]];
		},
		
	// CONNECTIONS
		getFriends: function () {
			return [user1, user2, user3];
		},
		
		getMutualFriends: function () {
			return [user2, user3];
		},
		
		getFriendsOfFriends: function () {
			return [user10, user11, user12, user13, user14];
		},
		
		getTopMatchmakers: function () {
			return [user3, user1, user0, user2];
		},

		getWinks: function () {
			// TODO
			return [];
		},

		getMyPossibleMatches: function () {
			// TODO
			return [];
		},

		getMatchingFriends: function () {
			// TODO
			return [];
		},

		getFacebookFriends: function () {
			// TODO
			console.log("TODO: bend over to Facebook");
			return [];
		},


	// ACTIVITIES
		getNotifications: function () {
			// TODO
			return [];
		},

		getSexyTimes: function () {
			// TODO
			return [];
		},
		
		getRecentActivities: function () {
			// TODO
			return [];
		},
		
		getWinks: function () {
			// TODO
			return [];
		},

		getRandomMatchIntro: function () {
			// TODO
			return [];
		},

		getRandomMessage: function () {
			// TODO
			return [];
		},

		getMessages: function () {
			// TODO
			return [];
		},

		getUnreadMessages: function () {
			// TODO
			return [];
		},

	// QUESTIONNAIRE
		getNewQuestions: function () {
			// TODO
			return [];
		},

		getAnswers: function () {
			// TODO
			return [];
		},


	};

});


/*
User: {
	name,
	email,
	fb_id,
	...
	...
	...
}

UserSummary: {
	name: String,
	id: String,
	photo: String
}

Activity: {
	id: String
	from: UserSummary,
	to: UserSummary,
	label: String, // For now just a text-only representation
	type: ActivityType
}

ActivityType: Number (SexyTime|Match|Wink)

Activity > Match: {
	matchmaker: UserSummary
}

Match > SexyTime: {
	notes: [Note],
	when: Date,
	where: String
}

Activity > Wink: {
}

MatchProposal {
	from: UserSummary,
	to: UserSummary
}

Note: {
	from: UserID,
	to: SexyTime,
	body: Text
}

Message: {
	from: UserSummary,
	to: UserSummary,
	body: String,
	status: ConversationStatus
}

Conversation: {
	status: ConversationStatus,
	messages: [Message]
}

ConversationSummary: {
	status: ConversationStatus,
	lastMessage: Message
}

ConversationStatus: Number

FacebookFriends: {
	TBD
}

PrivacySettings: [PrivacySetting]

PrivacySetting: {
	label: String,
	value: PrivacyFlag
}

PrivacyFlag: Number <Public|Private>

Question: { #fixed format
	id: id,
	string: question,
	category: <category>
	lang: language-code,
	answer1: String,
	answer2: String,
	answer3: String,
	answer4: String	
}

Answer: { #fixed format
	question: Question.id,
	answer: <0|1|2|3|4>
	explanation: String, #later!
	visibility: PrivacyFlag
}

<category>: String <about|identity|looks|lifestyle|relationship|background|personality|sexuality>
*/