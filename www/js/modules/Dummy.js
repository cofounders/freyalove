define(['Underscore'], function (_) {

/* USERS */

	// DIRECT FRIENDS

	var user1 = {
		"id": "1",
		"name": "Bette Porter",
		"dateOfBirth": "1975-04-12",
		"photo": "/dummy/user1.png",
		"about": "Bette Porter is a fictional character on the Showtime television network series The L Word, played by Jennifer Beals. While she is portrayed as the one true love of Tina Kennard, she is shown to be rather promiscuous and has had countless affairs with other women, whether or not she is with Tina. She was ranked No. 10 in AfterEllen.com's Top 50 Favorite Female TV Characters.",
		"points": "975",
		"location": "Los Angeles, US",
		"origin": "Los Angeles, US",
		"languages": "English, Spanish",
		"likes": "Michael Jackson, Angry Birds, Oracle Databases",
		"likeActivities": "Sleeping, Reading, Commodo, Sit Elit Sem, Fusce",
		"likeAthletes": "Serena Williams, Lance Armstrong, Sit Elit Sem, Fusce, Commodo, Sit Elit",
		"likeBooks": "Tolstoy, Elit Sem, Fusce, Commodo, Sit Elit Sem",
		"likeGames": "",
		"likePeople": "Nelson Mandela, Angelina Jolie, Commodo, Sit Elit Sem, Fusce, Commodo, Sit",
		"likeInterests": "",
		"likeMovies": "The Dark Knight, 2001: A Space Odyssey, A Bugs Life",
		"likeSportsTeams": "Barcelona, New York Yankees, Colorado Avalanche",
		"likeSports": "",
		"likeTv": "The L Word, Tom and Jerry, The Colbert Report, Knitting with Edna",
		"likeQuotes": "Carpe Diem"};
	var user2 = {
		"id": "2",
		"name": "Tina Kennard",
		"dateOfBirth": "1972-12-08",
		"photo": "/dummy/user2.png",
		"about": "Tina Kennard is a fictional character on the Showtime television network series The L Word, shown nationally in the United States. She is played by American actress Laurel Holloman. Tina lives in Los Angeles, California, and mostly hangs out in West Hollywood. She is the mother of Angelica Porter-Kennard and the on-off lover of Bette Porter.",
		"points": "1205",
		"location": "London, UK",
		"origin": "Los Angeles, US",
		"languages": "English",
		"likes": "Michael Jackson, Angry Birds, Oracle Databases",
		"likeActivities": "",
		"likeAthletes": "Serena Williams, Lance Armstrong, Sit Elit Sem, Fusce, Commodo, Sit Elit",
		"likeBooks": "Tolstoy, Elit Sem, Fusce, Commodo, Sit Elit Sem",
		"likeGames": "Uno, Fusce, Commodo, Sit Elit",
		"likePeople": "",
		"likeInterests": "Eating, Sleeping, Sem, Fusce, Commodo, Sit Elit Sem, Fusce, Commodo",
		"likeMovies": "The Dark Knight, 2001: A Space Odyssey, A Bugs Life",
		"likeSportsTeams": "",
		"likeSports": "Chess, Golf, Cycling, Minigolf, Pool, Darts, Rugby, Underwater Hockey",
		"likeTv": "The L Word, Tom and Jerry, The Colbert Report, Knitting with Edna",
		"likeQuotes": "Carpe Diem"};
	var user3 = {
		"id": "3",
		"name": "Alice Pieszecki",
		"dateOfBirth": "11/25/1976",
		"photo": "/dummy/user3.png",
		"about": "Alice Pieszecki is a fictional character on the Showtime television network series The L Word, shown nationally in the United States. She is played by American actress Leisha Hailey. Alice lives in Los Angeles, California, and mostly hangs out in West Hollywood. During the first seasons, she is often seen with her best friends, Shane McCutcheon (Katherine Moennig) and Dana Fairbanks (Erin Daniels).",
		"points": "201",
		"location": "Cape Town, ZA",
		"origin": "Prague, CZ",
		"languages": "English, Czech, Russian",
		"likes": "Michael Jackson, Angry Birds, Oracle Databases",
		"likeActivities": "Sleeping, Reading, Commodo, Sit Elit Sem, Fusce",
		"likeAthletes": "Serena Williams, Lance Armstrong, Sit Elit Sem, Fusce, Commodo, Sit Elit",
		"likeBooks": "",
		"likeGames": "Uno, Fusce, Commodo, Sit Elit",
		"likePeople": "",
		"likeInterests": "Eating, Sleeping, Sem, Fusce, Commodo, Sit Elit Sem, Fusce, Commodo",
		"likeMovies": "The Dark Knight, 2001: A Space Odyssey, A Bugs Life",
		"likeSportsTeams": "Barcelona, New York Yankees, Colorado Avalanche",
		"likeSports": "Chess, Golf, Cycling, Minigolf, Pool, Darts, Rugby, Underwater Hockey",
		"likeTv": "",
		"likeQuotes": ""};
	var user4 = {
		"id": "4",
		"name": "Anabelle Hernandez-Herrara",
		"dateOfBirth": "2/29/1984",
		"photo": "/dummy/user4.png",
		"about": "About Anabelle... Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam porta sem malesuada magna mollis euismod. Duis mollis, est non commodo luctus, nisi erat porttitor ligula, eget lacinia odio sem nec elit. Aenean eu leo quam. Pellentesque ornare sem lacinia quam venenatis vestibulum. Duis mollis, est non commodo luctus, nisi erat porttitor ligula, eget lacinia odio sem nec elit.",
		"points": "612",
		"location": "Cartagena, CO",
		"origin": "San Juan, CR",
		"languages": "Spanish, English, Italian",
		"likes": "Michael Jackson, Angry Birds, Oracle Databases",
		"likeActivities": "Sleeping, Reading, Commodo, Sit Elit Sem, Fusce",
		"likeAthletes": "",
		"likeBooks": "Tolstoy, Elit Sem, Fusce, Commodo, Sit Elit Sem",
		"likeGames": "Uno, Fusce, Commodo, Sit Elit",
		"likePeople": "Nelson Mandela, Angelina Jolie, Commodo, Sit Elit Sem, Fusce, Commodo, Sit",
		"likeInterests": "Eating, Sleeping, Sem, Fusce, Commodo, Sit Elit Sem, Fusce, Commodo",
		"likeMovies": "",
		"likeSportsTeams": "Barcelona, New York Yankees, Colorado Avalanche",
		"likeSports": "",
		"likeTv": "The L Word, Tom and Jerry, The Colbert Report, Knitting with Edna",
		"likeQuotes": "La vida es un carnaval."};

	// FRIENDS OF FRIENDS

	var user10 = {
		"id": "10",
		"name": "Kenny Shen",
		"dateOfBirth": "9/11/1982",
		"photo": "/dummy/user10.png",
		"about": "Kenny is a Python Wrangler... Cras justo odio, dapibus ac facilisis in, egestas eget quam. Vestibulum id ligula porta felis euismod semper. Maecenas sed diam eget risus varius blandit sit amet non magna.",
		"points": "502",
		"location": "Singapore, SG",
		"origin": "Singapore, SG",
		"languages": "English, Hokkien",
		"likes": "Michael Jackson, Angry Birds, Oracle Databases",
		"likeActivities": "",
		"likeAthletes": "Serena Williams, Lance Armstrong, Sit Elit Sem, Fusce, Commodo, Sit Elit",
		"likeBooks": "",
		"likeGames": "Uno, Fusce, Commodo, Sit Elit",
		"likePeople": "Nelson Mandela, Angelina Jolie, Commodo, Sit Elit Sem, Fusce, Commodo, Sit",
		"likeInterests": "",
		"likeMovies": "The Dark Knight, 2001: A Space Odyssey, A Bugs Life",
		"likeSportsTeams": "",
		"likeSports": "Chess, Golf, Cycling, Minigolf, Pool, Darts, Rugby, Underwater Hockey",
		"likeTv": "The L Word, Tom and Jerry, The Colbert Report, Knitting with Edna",
		"likeQuotes": "Do or do not, there is no try.\n\nLike is a circle to cycle around on."}
	var user11 = {
		"id": "11",
		"name": "Sayanee Basu",
		"dateOfBirth": "1985-03-22",
		"photo": "/dummy/user11.png",
		"about": "Sayanee is the Style Slinger... Cras justo odio, dapibus ac facilisis in, egestas eget quam. Vestibulum id ligula porta felis euismod semper. Maecenas sed diam eget risus varius blandit sit amet non magna.",
		"points": "234",
		"location": "Bali, ID",
		"origin": "Chennai, IN",
		"languages": "English, Tamil, Hindi",
		"likes": "Michael Jackson, Angry Birds, Oracle Databases",
		"likeActivities": "Sleeping, Reading, Commodo, Sit Elit Sem, Fusce",
		"likeAthletes": "",
		"likeBooks": "Tolstoy, Elit Sem, Fusce, Commodo, Sit Elit Sem",
		"likeGames": "",
		"likePeople": "Nelson Mandela, Angelina Jolie, Commodo, Sit Elit Sem, Fusce, Commodo, Sit",
		"likeInterests": "Eating, Sleeping, Sem, Fusce, Commodo, Sit Elit Sem, Fusce, Commodo",
		"likeMovies": "The Dark Knight, 2001: A Space Odyssey, A Bugs Life",
		"likeSportsTeams": "Barcelona, New York Yankees, Colorado Avalanche",
		"likeSports": "Chess, Golf, Cycling, Minigolf, Pool, Darts, Rugby, Underwater Hockey",
		"likeTv": "",
		"likeQuotes": "Carpe Diem.\n\nThe early bird catches the early worm."};
	var user12 = {
		"id": "12",
		"name": "Sebastiaan Deckers",
		"dateOfBirth": "1/19/1983",
		"photo": "/dummy/user12.png",
		"about": "Seb is the Javascript Jockey... Cras justo odio, dapibus ac facilisis in, egestas eget quam. Vestibulum id ligula porta felis euismod semper. Maecenas sed diam eget risus varius blandit sit amet non magna.",
		"points": "371",
		"location": "Melbourne, AU",
		"origin": "Bruxelles, BE",
		"languages": "English, Flemish, French",
		"likes": "Michael Jackson, Angry Birds, Oracle Databases",
		"likeActivities": "Sleeping, Reading, Commodo, Sit Elit Sem, Fusce",
		"likeAthletes": "Serena Williams, Lance Armstrong, Sit Elit Sem, Fusce, Commodo, Sit Elit",
		"likeBooks": "Tolstoy, Elit Sem, Fusce, Commodo, Sit Elit Sem",
		"likeGames": "Uno, Fusce, Commodo, Sit Elit",
		"likePeople": "",
		"likeInterests": "Eating, Sleeping, Sem, Fusce, Commodo, Sit Elit Sem, Fusce, Commodo",
		"likeMovies": "",
		"likeSportsTeams": "Barcelona, New York Yankees, Colorado Avalanche",
		"likeSports": "Chess, Golf, Cycling, Minigolf, Pool, Darts, Rugby, Underwater Hockey",
		"likeTv": "The L Word, Tom and Jerry, The Colbert Report, Knitting with Edna",
		"likeQuotes": "Ceterum censeo Carthaginem deletam esse."};
	var user13 = {
		"id": "13",
		"name": "Veronica Ng",
		"dateOfBirth": "8/1/1983",
		"photo": "/dummy/user13.png",
		"about": "Veronica is the UI Undertaker... Cras justo odio, dapibus ac facilisis in, egestas eget quam. Vestibulum id ligula porta felis euismod semper. Maecenas sed diam eget risus varius blandit sit amet non magna.",
		"points": "290",
		"location": "Kota Kinabalu, MY",
		"origin": "Singapore, SG",
		"languages": "English, Swahili",
		"likes": "Michael Jackson, Angry Birds, Oracle Databases",
		"likeActivities": "Sleeping, Reading, Commodo, Sit Elit Sem, Fusce",
		"likeAthletes": "Serena Williams, Lance Armstrong, Sit Elit Sem, Fusce, Commodo, Sit Elit",
		"likeBooks": "",
		"likeGames": "Uno, Fusce, Commodo, Sit Elit",
		"likePeople": "",
		"likeInterests": "Eating, Sleeping, Sem, Fusce, Commodo, Sit Elit Sem, Fusce, Commodo",
		"likeMovies": "The Dark Knight, 2001: A Space Odyssey, A Bugs Life",
		"likeSportsTeams": "Barcelona, New York Yankees, Colorado Avalanche",
		"likeSports": "",
		"likeTv": "The L Word, Tom and Jerry, The Colbert Report, Knitting with Edna",
		"likeQuotes": "All for one, one for all."};
	var user14 = {
		"id": "14",
		"name": "Wolfgang Maehr",
		"dateOfBirth": "7/25/1982",
		"photo": "/dummy/user14.png",
		"about": "Wolf is the IXD Imp... Cras justo odio, dapibus ac facilisis in, egestas eget quam. Vestibulum id ligula porta felis euismod semper. Maecenas sed diam eget risus varius blandit sit amet non magna.",
		"points": "103",
		"location": "Istambul, TR",
		"origin": "Vienna, AT",
		"languages": "English, German",
		"likes": "Michael Jackson, Angry Birds, Oracle Databases",
		"likeActivities": "Sleeping, Reading, Commodo, Sit Elit Sem, Fusce",
		"likeAthletes": "",
		"likeBooks": "Tolstoy, Elit Sem, Fusce, Commodo, Sit Elit Sem",
		"likeGames": "Uno, Fusce, Commodo, Sit Elit",
		"likePeople": "Nelson Mandela, Angelina Jolie, Commodo, Sit Elit Sem, Fusce, Commodo, Sit",
		"likeInterests": "",
		"likeMovies": "",
		"likeSportsTeams": "Barcelona, New York Yankees, Colorado Avalanche",
		"likeSports": "Chess, Golf, Cycling, Minigolf, Pool, Darts, Rugby, Underwater Hockey",
		"likeTv": "The L Word, Tom and Jerry, The Colbert Report, Knitting with Edna",
		"likeQuotes": "Jedem Tierchen sein Pläsierchen."};

	// OTHER USERS - Profile Summary
	var user20 = {
		"id": "20",
		"name": "Amy Hunting",
		"photo": "/dummy/user20.png"};
	var user21 = {
		"id": "21",
		"name": "Adrianna Svitak",
		"photo": "/dummy/user21.png"};
	var user22 = {
		"id": "22",
		"name": "Greta Howell",
		"photo": "/dummy/user22.png"};

	// MYSELF
		var user0 = {
		"id": "0",
		"name": "Jenny Schecter",
		"dateOfBirth": "1979-05-26",
		"photo": "/dummy/user0.png",
		"about": "Jennifer Schecter is a fictional character origin the American Showtime television drama series The L Word, played by Mia Kirshner. Jenny debuted on-screen during the pilot episode and remained until the series' final episode. Jenny became well documented in the media for her outlandish plots. Jenny was created by series creator Ilene Chaiken, based on herself as a younger woman living in the lesbian community.",
		"points": "702",
		"location": "Beijing, CN",
		"origin": "Los Angeles, US",
		"languages": "English, French",
		"likes": "Michael Jackson, Angry Birds, Oracle Databases",
		"likeActivities": "Sleeping, Reading, Commodo, Sit Elit Sem, Fusce",
		"likeAthletes": "Serena Williams, Lance Armstrong, Sit Elit Sem, Fusce, Commodo, Sit Elit",
		"likeBooks": "",
		"likeGames": "Uno, Fusce, Commodo, Sit Elit",
		"likePeople": "Nelson Mandela, Angelina Jolie, Commodo, Sit Elit Sem, Fusce, Commodo, Sit",
		"likeInterests": "",
		"likeMovies": "The Dark Knight, 2001: A Space Odyssey, A Bugs Life",
		"likeSportsTeams": "Barcelona, New York Yankees, Colorado Avalanche",
		"likeSports": "Chess, Golf, Cycling, Minigolf, Pool, Darts, Rugby, Underwater Hockey",
		"likeTv": "",
		"likeQuotes": "Carpe Diem",
		"friends": [user1, user2, user3, user4, user10, user11, user12, user12]};

	var allUsers = [user0, user1, user2, user3, user4, user10, user11, user12, user12, user14, user20, user21, user22];
	var allOthers = [user0, user1, user2, user3, user4, user10, user11, user12, user12, user14, user20, user21, user22];
	var allUsersById = {0: user0, 1: user1, 2: user2, 3: user3, 4: user4, 10: user10, 11: user11, 12: user12, 13: user13, 14: user14, 20: user20, 21: user21, 22: user22};
	var allProfiles = [user0, user1, user2, user3, user4, user10, user11, user12, user12, user14];

	var userToUserSummary = function (user) {
			return {
				id: user.id,
				name: user.name,
				photo: user.photo
			};
		}
	var allUsersSummary = allUsers.map(userToUserSummary);
	var allOthersSummary = allOthers.map(userToUserSummary);
	// var allUsersByIdSummary = allUsersById.map(userToUserSummary);
	var allProfilesSummary = allProfiles.map(userToUserSummary);

/* ACTIVITIES */

/*
	var activity = {
		"id": "0",
		"from": user0,
		"to": user0,
		"type": "match|sexytime|wink"}*/

	var wink0 = {
		"id": "0",
		"from": user1,
		"to": user0,
		"type": "wink",
		"seen": false};
	var wink1 = {
		"id": "1",
		"from": user4,
		"to": user0,
		"type": "wink",
		"seen": true};
	var wink2 = {
		"id": "2",
		"from": user12,
		"to": user0,
		"type": "wink",
		"seen": false};
	var wink3 = {
		"id": "3",
		"from": user13,
		"to": user0,
		"type": "wink",
		"seen": true};
	var wink4 = {
		"id": "4",
		"from": user20,
		"to": user0,
		"type": "wink",
		"seen": false};

	var allWinks = [wink0, wink1, wink2, wink3, wink4];

	var match0 = {
		"id": "0",
		"from": user2,
		"to": user0,
		"type": "match",
		"matchmaker": user3};
	var match1 = {
		"id": "1",
		"from": user3,
		"to": user0,
		"type": "match",
		"matchmaker": user10};
	var match2 = {
		"id": "2",
		"from": user11,
		"to": user0,
		"type": "match",
		"matchmaker": user1};
	var match3 = {
		"id": "3",
		"from": user14,
		"to": user0,
		"type": "match",
		"matchmaker": user22};
	var match4 = {
		"id": "4",
		"from": user21,
		"to": user0,
		"type": "match",
		"matchmaker": user2};

	var allMatches = [match0, match1, match2, match3, match4];

	var sexytime0 = {
		"id": "0",
		"from": user2,
		"to": user0,
		"type": "sexytime",
		"when": "THU, 19:00",
		"where": "Somerset 313",
		"notes": [{"from": user0, "body": "Great!"}, {"from": user2, "body": "See you! x"}],
		"rsvp": false};
	var sexytime1 = {
		"id": "1",
		"from": user3,
		"to": user0,
		"type": "sexytime",
		"when": "FRI, 12:00",
		"where": "Bugis MRT",
		"notes": [],
		"rsvp": true};
	var sexytime2 = {
		"id": "2",
		"from": user11,
		"to": user0,
		"type": "sexytime",
		"when": "SAT, 09:00",
		"where": "Music Cafe at the Park",
		"notes": [{"from": user11, "body": "Sorry, reschedule to 10:00 as it's really early for a Saturday?"}, {"from": user0, "body": "Or we just have breakfast in bed instead? ;)"}],
		"rsvp": null};
	var sexytime3 = {
		"id": "3",
		"from": user14,
		"to": user0,
		"type": "sexytime",
		"when": "SUN, 21:00",
		"where": "The Great Wall of China",
		"notes": [{"from": user0, "body": "Always wanted to see it! <3"}],
		"rsvp": null};
	var sexytime4 = {
		"id": "4",
		"from": user21,
		"to": user0,
		"type": "sexytime",
		"when": "MON, 20:00",
		"where": "Somerset 313",
		"notes": [],
		"rsvp": true};

	var allSexytimes = [sexytime0, sexytime1, sexytime2, sexytime3, sexytime4];



/*

MatchProposal {
	origin: UserSummary,
	to: UserSummary
}

*/


/* MESSAGES */

/* Schemas:

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
*/

var ConversationStatus = {
	UNREAD: 1,
	READ: 2
};
var message1 = {
		from: user20,
		to: user21,
		body: 'Stop talking, brain thinking. Hush.',
		status: ConversationStatus.UNREAD,
		when: '100 days ago'
	},
	message2 = {
		from: user21,
		to: user20,
		body: 'I won\'t stand for it. Not now, not ever, do you understand me?!',
		status: ConversationStatus.UNREAD,
		when: 'yesterday'
	},
	message3 = {
		from: user22,
		to: user21,
		body: 'Well, they call me the Doctor. I don\'t know why.',
		status: ConversationStatus.UNREAD,
		when: 'today'
	},
	message4 = {
		from: user22,
		to: user21,
		body: 'All I\'ve got to do is pass as an ordinary human being. Simple. What could possibly go wrong?',
		status: ConversationStatus.READ,
		when: 'yesterday'
	},
	message5 = {
		from: user22,
		to: user21,
		body: 'Simple.',
		status: ConversationStatus.UNREAD,
		when: '10 days ago'
	},
	message6 = {
		from: user22,
		to: user21,
		body: 'What could possibly go wrong?',
		status: ConversationStatus.READ,
		when: '2 days ago'
	};

var conversationSummary1 = {
		status: ConversationStatus.UNREAD,
		lastMessage: message6
	},
	conversationSummary2 = {
		status: ConversationStatus.READ,
		lastMessage: message2
	};


/* QUESTIONNAIRE
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

	// Calculate years of age from a date to current time
	function getAge(dateString) {
		var today = new Date();
		var birthDate = new Date(dateString);
		var age = today.getFullYear() - birthDate.getFullYear();
		var m = today.getMonth() - birthDate.getMonth();
		if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
			age--;
		}
		return age;
	}

	allProfiles.forEach(function(profile) {
		if (!profile.age) {
			profile.age = getAge(profile.dateOfBirth);
		}
	});

	// random integer generator 0 <= x <= i | (i=1)
	function randInt(i) {
		if (isNaN(i))
			i = 2;
		return Math.floor(Math.random()*i);
	};

	// randomiser sorting function
	function randOrd(){
		return (Math.round(Math.random())-0.5);
	};

	// randomises an array
	function randArray(array) {
		return _.shuffle(array);
	};


// PUBLIC FUNCTIONS
	return {

	// USERS
		getAllUsers: function() {
			return allUsers;
		},

		getMyProfile: function () {
			return user0;
		},

		getProfile: function (id) {
			return allUsersById[id];
		},

		getRandomProfile: function() {
			return allUsers[randInt(allUsers.length)];
		},

	// CONNECTIONS
		getFriends: function () {
			return randArray(user0.friends);
		},

		getMutualFriends: function () {
			return randArray(user0.friends).splice(0, randInt(user0.friends.length));
		},

		getFriendsOfFriends: function () {
			return randArray([user10, user11, user12, user13, user14, user20, user21, user22]);
		},

		getTopMatchmakers: function () {
			return [user2, user1, user0, user4, user3];
		},

		getMyPossibleMatches: function () {
			return randArray(allProfiles).slice(0, 6);
		},

		getMatchingFriends: function () {
			var first = randArray(allOthersSummary),
				second = randArray(allOthersSummary),
				matchProposals = [];
			for (var i = 0; i < first.length; i++) {
				matchProposals.push({
					first: first[i],
					second: second[i]
				});
			}
			return matchProposals;
		},

		getFacebookFriends: function () {
			// TODO
			console.log("TODO: bend over to Facebook");
			return randArray([user20, user21, user22]);
		},


	// ACTIVITIES
		getNotifications: function () {
			// TODO
			return [];
		},

		getSexyTimes: function () {
			if (randInt() > 0)
				return randArray(allSexytimes);
			return [];
		},

		getRecentActivities: function () {
			// TODO
			return [];
		},

		getWinks: function () {
			return randArray(allWinks);
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
			return [conversationSummary1, conversationSummary2];
		},

		getConversation: function () {
			return {
				id: '123',
				status: ConversationStatus.UNREAD,
				participants: [
					message4.to,
					message4.from
				],
				messages: [
					message3,
					message4,
					message5,
					message6
				]
			};
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

	// STREAM
		getStreamUnread: function () {
			return {
				unreadNotifications: randInt(20),
				unreadConversations: randInt(),
				unreadSexyTimes: randInt(5)
			};
		}

	};

});
